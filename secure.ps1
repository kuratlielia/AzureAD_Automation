$username = "eliakuratli@solonweb.onmicrosoft.com"
$password = "SXfyXfCy&noci5Lc" | ConvertTo-SecureString -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($username, $password)
$credential | Export-Clixml -Path "C:\temp\credentials.xml"