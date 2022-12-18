# chango-postfix-policy
**Postfix custom policy to check authenticated user membership within an Active Directory group before allowing to send email.**

It reads *sasl_username* attribute and checks against Active Directory if the user is member of the configured AD group


## Prerequisites 
1) Python +3.5
2) Postfix server must already be added in Active Directory (either with SSSD or Samba)
3) getent command should be present and functional in postfix server. `getent group someADgroup` should respond current members.

## Initial Config
1) Download script `git clone https://github.com/changoz/chango-postfix-policy.git /opt/chango-postfix-policy`

2) Execute: `whereis python`. If applicable, replace python path at py scripts first line `#!/usr/bin/python3.9`

3) Replace Active Directory group to search for, at py script line 11. Note that the group should'nt have realm nor domain (i.e.: 'managers')

```
adgroup = 'group_without_realm'
```

4) Check the script output before applying postfix configuration. Execute at shell `echo sasl_username=user_to_test | /opt/chango-postfix-policy/chango-policy.py`
It should reply with `action=dunno` or `action=rejected`. Depends on user and AD group user.

5) Folder permissions: `chown nobody /opt/chango-postfix-policy`

## Postfix configuration 
### 1) master.cf

#### as tcp Listener
/etc/postfix/master.cf:

```
127.0.0.1:9998  inet  n       n       n       -       0       spawn
     user=nobody argv=/opt/chango-postfix-policy/chango-policy.py
```

### 2) main.cf
#### as tcp Listener

/etc/postfix/main.cf:

```
smtpd_recipient_restrictions =
       ...
       reject_unauth_destination
       check_policy_service inet:127.0.0.1:9998
       ...
```

### Troubleshooting
1) Enable verbose at postfix main.cf to get detailed logs. Python error trace should be logged at /var/log/maillog. Read [Postfix Oficial Verbose Logging] (http://www.postfix.org/DEBUG_README.html)

2) Wrong python identation. Use autopep8 to format chango-policy.py script: `autopep8 -i chango-policy.py`

3) Test email by using command line with `openssl s_client -starttls smtp -ign_eof -crlf -connect your_server:25`

```
EHLO server
AUTH LOGIN
base64 ad_user_login_without_realm (enter)
base65 ad_user_password (enter)
mail from: user@some.com
rcpt to: dest@some.com
data
subject: some subject
test
.
```

### Extras
* [Base64 online tool] (https://www.base64encode.org/) 
* Thanks to [Mat1010] (https://github.com/mat1010/postfix-python-policy-service)
