# requirements
    
   * awsume - https://github.com/trek10inc/awsume
   * awscli - https://github.com/aws/aws-cli
   * terraform -  https://www.terraform.io/downloads.html

## versions

    [klang@bascule cloudhealth]$ python --version
    Python 3.6.5
    
    [klang@bascule cloudhealth]$ awsume -v
    3.2.8
    
    [klang@bascule cloudhealth]$ aws --version
    aws-cli/1.15.20 Python/3.6.5 Darwin/17.7.0 botocore/1.10.20
    
    [klang@bascule cloudhealth]$ terraform version
    Terraform v0.11.8
    + provider.aws v1.34.0

## aws configuration

Assuming an AWS multi account setup, with an `iam` account for user handling and trust relationships created to a
range of accounts.

    aws configure set region eu-west-1 --profile iam
    aws configure set aws_access_key_id <AWS_ACCESS_KEY_ID>  --profile iam
    aws configure set aws_secret_access_key <AWS_SECRET_ACCESS_KEY>  --profile iam

    # at this point, account information can be requested without the use of an MFA code
    mfa_serial=$(aws iam list-mfa-devices | jq .MFADevices[].SerialNumber)
    mfa_serial=${mfa_serial//\"/}

    aws configure set mfa_serial $mfa_serial --profile iam
    # at this point, interaction with the profile has to be followed with an MFA code

For `aws-cli` interaction to trusted accounts

    mfa_serial=$(aws configure get mfa_serial)
    aws configure set region eu-west-1 --profile AccountAlias
    aws configure set role_arn arn:aws:iam::AccountID:role/AccessRole --profile AccountAlias
    aws configure set source_profile iam --profile AccountAlias
    aws configure set mfa_serial $mfa_serial --profile AccountAlias

Where `AccountID`, `AccountAlias`, `AccessRole` are defined as.

   - AccountID     - the 12 digit AWS Account ID uniquely identifying an account
   - AccountAlias  - if the account has an alias, otherwise repeat the AccountID
   - AccessRole    - a role on the account, that has permissions to create roles (typically AdministratorAccess)

# usage

## preparation 

`accounts-with-cloudmanager.txt` - List of "AccountID AccountAlias AccessRole" that need to allow CloudHealth access via 
a role. 
 
## execution

Add the account numbers to the `accounts_with_cloudmanager.txt` file

    awsume iam
    python init-cloudmanager.py
    terraform init
    terraform plan
    terraform apply -auto-approve

It's possible to verify the presence of the account role [here](https://console.aws.amazon.com/iam/home?region=eu-west-1#/roles/cloudpartners-cloudmanager),
if you are logged into the AWS console.
