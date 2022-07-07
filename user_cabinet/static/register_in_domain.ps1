if (!(Get-Module -ListAvailable -Name ActiveDirectory))
{
    Write-Warning "This function needs Active Directory module! Please import it or get it from https://github.com/samratashok/ADModule"
}

function Generate-Password {
    -join ('abcdefghkmnrstuvwxyzABCDEFGHKLMNPRSTUVWXYZ23456789$%&#()[]{}?!@'.ToCharArray() | Get-Random -Count 32)
}

#Create Computer
$NewComputerName = 'DCSonarWorkstation'
try
{
    Remove-ADComputer -Identity $NewComputerName -Confirm:$False
}
catch
{
    Write-Output ""
}
$PasswordComputer = Generate-Password
New-ADComputer -Name $NewComputerName -AccountPassword (ConvertTo-SecureString -String $PasswordComputer -AsPlainText -Force) -PasswordNeverExpires $true

#Grant DCSYNC privilages
$SamAccountName = $NewComputerName + '$'
$baseDN = (Get-ADRootDSE).defaultNamingContext
$HostName = (Get-ADDomainController).HostName


Get-PSDrive | ForEach {

    If ($_.Name -eq 'AD1')
    {

        Remove-PSDrive -Name $_.Name

    }

}

$AD = (New-PSDrive -Name 'AD1' -PSProvider ActiveDirectory -Server $HostName -root "//RootDSE/").Name
$Path = $AD + ':\' + $baseDN
$ACL = Get-Acl -Path $Path
$sid = New-Object System.Security.Principal.NTAccount($SamAccountName)

# DS-Replication-Get-Changes
$objectGuidGetChanges = New-Object Guid 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2
$ACEGetChanges = New-Object DirectoryServices.ActiveDirectoryAccessRule($sid, 'ExtendedRight', 'Allow', $objectGuidGetChanges)
$ACL.AddAccessRule($ACEGetChanges)
# DS-Replication-Get-Changes-All
$objectGuidGetChangesAll = New-Object Guid 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2
$ACEGetChangesAll = New-Object DirectoryServices.ActiveDirectoryAccessRule($sid, 'ExtendedRight', 'Allow', $objectGuidGetChangesAll)
$ACL.AddAccessRule($ACEGetChangesAll)
# DS-Replication-Get-Changes-In-Filtered-Set
$objectGuidGetChangesFiltered = New-Object Guid 89e95b76-444d-4c62-991a-0facbeda640c
$ACEGetChangesFiltered = New-Object DirectoryServices.ActiveDirectoryAccessRule($sid, 'ExtendedRight', 'Allow', $objectGuidGetChangesFiltered)
$ACL.AddAccessRule($ACEGetChangesFiltered)
Write-Verbose "Setting ACL for $( $baseDN ) for $( $SamAccountName ) to use $( $GUIDRight ) right."
Set-Acl $Path -AclObject $ACL

$NewUserName = 'DCSonarUser'
# Clear previous User if it exists
try
{
    Remove-ADUser -Identity $NewUserName -Confirm:$False
}
catch
{
    Write-Output ""
}
$PasswordUser = Generate-Password
New-ADUser -Name $NewUserName -AccountPassword (ConvertTo-SecureString -String $PasswordUser -AsPlainText -Force) -PasswordNeverExpires $true -Enabled $True

Write-Output @"
============================
Domain:                 $( (Get-ADDomain).Name )
HostName:               $( $HostName )
BaseDN:                 $( $baseDN )
WorkstationName:        $( $SamAccountName )
WorkstationPassword:    $( $PasswordComputer )
UserDN:                 $( (Get-ADUser -Identity $NewUserName).DistinguishedName )
UserPassword:           $( $PasswordUser )
============================
"@