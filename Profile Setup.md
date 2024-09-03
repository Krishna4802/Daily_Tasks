# Profile Setup



vi .zprofile
source ~/.zprofile
source ~/.bash_profile


 
vi .pgpass
for db :
Host:port:db:user_name:password
 
After this

 
vi ~/.zshrc
fordb:
Alias alias_name=“psql -h -d -u “
for machine:
alias alias_name="machine login method(ssh <username>@dev-pth")
source ~/.zshrc
 
