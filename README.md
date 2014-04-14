Fail2ban
========

Install fail2ban service and configure jails.

This role doesn't touch any upstream provided files. All configuration parts
are placed in fail2ban's .local files.

If [`sbitmedia.monit`](https://github.com/sbitmedia/ansible-monit) role is
available, a Monit check will be placed.

Requirements
------------

Tested on Debian wheezy and CentOS 6. Likely it works in other versions of
Debian and Ubuntu.

Role Variables
--------------

Look `defaults/main.yml` for variables you can override.

Example definition of jails:

```yaml
fail2ban_jails:
  ssh-iptables:
    enabled  : true
    filter   : sshd
    action   : |
      iptables[name=SSH, port=ssh, protocol=tcp]
      sendmail-whois[name=SSH, dest=root, sender=fail2ban@example.com, sendername="Fail2Ban"]
    logpath  : /var/log/secure
    maxretry : 5
```

Dependencies
------------

None.

Example Playbook
-------------------------

```yaml
- hosts: servers
  roles:
     - { role: jonhattan.fail2ban }
```

License
-------

BSD

Author Information
------------------

Jonathan Araña Cruz - SB IT Media, S.L.

