Fail2ban
========

Install fail2ban service and configure jails.

Requirements
------------

Tested on Debian wheezy and CentOS 6. Likely it works in other versions of Debian and Ubuntu.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Look `defaults/main.yml` for variables you can override.

Jails are defined as:

`
fail2ban_jails:
  ssh-iptables:
    enabled  : true
    filter   : sshd
    action   : |
      iptables[name=SSH, port=ssh, protocol=tcp]
      sendmail-whois[name=SSH, dest=root, sender=fail2ban@example.com, sendername="Fail2Ban"]
    logpath  : /var/log/secure
    maxretry : 5
`

Dependencies
------------

None.

Example Playbook
-------------------------

    - hosts: servers
      roles:
         - { role: sbitmedia.fail2ban }

License
-------

BSD

Author Information
------------------

Jonathan Araña Cruz - SB IT Media, S.L.

