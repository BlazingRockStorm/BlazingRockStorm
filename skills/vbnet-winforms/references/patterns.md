# VB.NET WinForms — code patterns

Generic snippets to copy when adding code to a VB.NET WinForms app on the .NET Framework.
Class/variable names are illustrative — rename to match the repo. Always follow the
conventions of the file you are editing.

Each pattern notes **"When porting"** — how the idiom maps to a modern target language if you
are rebuilding the app elsewhere (see the SKILL's *Reading & porting* section).

## 1. File skeleton

```vb
Option Strict On
Imports System.Data.SqlClient

Public Class SqlHelper

#Region "ExecuteNonQuery"
    ''' <summary>
    ''' Runs a DML statement; returns -1 on error (does not throw).
    ''' </summary>
    ''' <param name="cmd"></param>
    ''' <returns></returns>
    ''' <remarks></remarks>
    Public Shared Function ExecNonQuery(ByVal cmd As SqlCommand) As Integer
        Dim retAns As Integer = 0
        Try
            retAns = cmd.ExecuteNonQuery()
        Catch ex As Exception
            LogHelper.WriteError(ex.ToString())
            retAns = -1
        End Try
        Return retAns
    End Function
#End Region

End Class
```

**When porting:** drop `Option Strict`/`#Region`/single-return scaffolding; let the helper
throw and catch at a boundary, or return a `Result` type.

## 2. Static DB-access class + transaction

```vb
Public Class DbAccess

    Public Shared Conn As SqlConnection
    Public Shared Tran As SqlTransaction

    ' Open the connection and begin a transaction
    Public Sub ConnStart(ByVal connStr As String)
        Conn = New SqlConnection(connStr)
        Conn.Open()
        Tran = Conn.BeginTransaction()
    End Sub

    ' Commit on success, roll back on failure; always close the connection
    Public Sub ConnEnd(ByVal isSuccess As Boolean)
        If Tran IsNot Nothing Then
            If isSuccess Then
                Tran.Commit()
            Else
                Tran.Rollback()
            End If
        End If
        If Conn IsNot Nothing Then
            Conn.Close()
            Conn.Dispose()
        End If
    End Sub

    ' Commit mid-run and start a new transaction (batching)
    Public Sub ConnCommit(ByVal isSuccess As Boolean)
        If isSuccess Then Tran.Commit() Else Tran.Rollback()
        Tran = Conn.BeginTransaction()
    End Sub

End Class
```

**When porting:** the shared static `Conn`/`Tran` is a global; replace with a scoped
connection / unit-of-work per operation (`using`/context manager). Keep the commit-on-success
/ rollback-on-failure *semantics* — that is behavior, not style.

## 3. Usage flow: ConnStart / Try-Finally / ConnEnd

```vb
Private Function DoJob() As Boolean
    Dim retAns As Boolean = True
    Dim db As New DbAccess

    Call db.ConnStart(GetConnStr())
    Try
        If Not Work() Then
            retAns = False
            Exit Try
        End If
    Catch ex As Exception
        LogHelper.WriteError(ex.ToString())
        retAns = False
    Finally
        Call db.ConnEnd(retAns)   ' True -> Commit, False -> Rollback
    End Try
    Return retAns
End Function
```

Dry-run mode: have `ConnEnd` check a flag (radio button) — commit only when the user opts in,
default to rollback so real data is never touched.

**When porting:** `Try/Finally` + `ConnEnd(success)` becomes a transaction scope that commits
at the end of the happy path and rolls back on exception. Preserve the dry-run toggle.

## 4. Connection string from My.Settings (Test/Production split)

```vb
Private Function GetConnStr() As String
    Dim user As String = ""
    Dim pass As String = ""
    Dim db As String = ""
    Dim server As String = ""

    If rdoTest.Checked Then
        user = My.Settings.UserID
        pass = My.Settings.Password
        db = My.Settings.Database
        server = My.Settings.ServerName
    ElseIf rdoProduction.Checked Then
        user = My.Settings.UserID_Production
        pass = My.Settings.Password_Production
        db = My.Settings.Database_Production
        server = My.Settings.ServerName_Production
    End If

    ' strBase = template "Server={3};Database={2};User Id={0};Password={1};"
    Return String.Format(strBase, user, pass, db, server)
End Function
```

Never hardcode credentials in source; read them from `My.Settings`/config.

**When porting:** `My.Settings` is an XML app-config file; move secrets to environment
variables / a secret manager, and keep the Test/Production separation.

## 5. Run SELECT/DML via helpers (check the sentinel)

```vb
' SELECT -> DataSet; helper returns Nothing on error
Dim ds As DataSet = SqlHelper.FillDataSet(cmd)
If ds Is Nothing OrElse ds.Tables.Count = 0 Then
    Return False
End If

' DML -> Integer, -1 on error
If SqlHelper.ExecNonQuery(cmd) < 0 Then
    Return False
End If
```

**When porting:** replace sentinel checks with exceptions or an explicit `Result`/`Option`
type; a `DataSet` typically becomes a list of typed records.

## 6. Parameterize (injection-safe)

```vb
Dim cmd As New SqlCommand("SELECT * FROM t_customer WHERE cd = @cd", Conn, Tran)
cmd.Parameters.AddWithValue("@cd", inputCd)
Dim ds As DataSet = SqlHelper.FillDataSet(cmd)
```

**When porting:** keep parameterization — every target's DB client has parameter binding.
Never interpolate user values into SQL.

## 7. File logging (fixed encoding, append, timestamp)

```vb
Public Shared Sub WriteText(ByVal path As String, ByVal txt As String)
    ' Append, UTF-16 (change encoding to match the repo if needed)
    Using sw As New System.IO.StreamWriter(path, True, New System.Text.UnicodeEncoding(False, False))
        sw.WriteLine(Now.ToString("HH:mm:ss") & " | " & txt)
    End Using
End Sub
```

**When porting:** use the target's logging framework with levels; only preserve the file
**encoding** if downstream tools consume the log files.

## 8. Debug-only conditional compilation

```vb
#If DEBUG Then
    Dim sql As String = cmd.CommandText
    For Each p As SqlParameter In cmd.Parameters
        sql = sql.Replace(p.ParameterName, CStr(p.Value))
    Next
    LogHelper.WriteText(logPath, sql)
#End If
```

**When porting:** `#If DEBUG` becomes a debug/trace log level, not a compile-time switch.

## Build

```
msbuild <Project>.vbproj /p:Configuration=Debug   /p:Platform=x86
msbuild <Project>.vbproj /p:Configuration=Release /p:Platform=x86
```

Repeat for every platform (`AnyCPU`/`x64`) the project uses. Or build in Visual Studio.
If there are copy-to-output assets, build **every** configuration to avoid stale copies.
