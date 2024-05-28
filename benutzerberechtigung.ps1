# Importiere das AzureAD-Modul
Import-Module AzureAD

# Lade die Anmeldeinformationen aus den Umgebungsvariablen
$username = $env:AZURE_AD_USERNAME
$password = $env:AZURE_AD_PASSWORD | ConvertTo-SecureString -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $password

# Authentifiziere bei Azure AD
Connect-AzureAD -Credential $credential

# Pfad zur CSV-Datei
$csvPath = ".\benutzerberechtigung.csv"

# Lese die CSV-Datei ein
$users = Import-Csv -Path $csvPath

# Durchlaufe jeden Benutzer in der CSV-Datei
foreach ($user in $users) {
    # Finde den Benutzer in Azure AD
    $aadUser = Get-AzureADUser -Filter "UserPrincipalName eq '$($user.Email)'"

    # Wenn der Benutzer in Azure AD existiert
    if ($aadUser) {
        # Durchlaufe alle Header in der CSV-Datei
        foreach ($header in $user.PSObject.Properties.Name) {
            # Überspringe die Spalten für Benutzername und Email
            if ($header -eq "Benutzername" -or $header -eq "Email") {
                continue
            }

            # Finde die Gruppe in Azure AD
            $group = Get-AzureADGroup -Filter "DisplayName eq '$header'"

            if ($group) {
                # Überprüfe den Wert für die Gruppe
                if ($user.$header -eq "True") {
                    # Füge den Benutzer zur Gruppe hinzu, wenn er nicht bereits Mitglied ist
                    if (-not (Get-AzureADGroupMember -ObjectId $group.ObjectId | Where-Object { $_.ObjectId -eq $aadUser.ObjectId })) {
                        Add-AzureADGroupMember -ObjectId $group.ObjectId -RefObjectId $aadUser.ObjectId
                        Write-Output "Benutzer $($user.'Email') zur Gruppe $header hinzugefügt."
                    }
                } elseif ($user.$header -eq "False") {
                    # Entferne den Benutzer aus der Gruppe, wenn er Mitglied ist
                    if (Get-AzureADGroupMember -ObjectId $group.ObjectId | Where-Object { $_.ObjectId -eq $aadUser.ObjectId }) {
                        Remove-AzureADGroupMember -ObjectId $group.ObjectId -MemberId $aadUser.ObjectId
                        Write-Output "Benutzer $($user.'Email') aus der Gruppe $header entfernt."
                    }
                }
            } else {
                Write-Output "Gruppe $header nicht in Azure AD gefunden."
            }
        }
    } else {
        Write-Output "Benutzer $($user.'Email') nicht in Azure AD gefunden."
    }
}

# Trennen der Azure AD Sitzung
Disconnect-AzureAD
