Fail2ban
========

Performs installation and configuration of Fail2ban service.

Provides an action plugin to facilitate configuration of jails. See below for
details.

This role is Work In Progress. See [`TODO` file](TODO.md) for some details.

This role doesn't touch any upstream provided files. All configuration parts
are placed in fail2ban's `.local` files.

In RedHat systems, `jail.local` is shipped with some goodies picked from
Debian's `jail.conf`, to ease management of actions.

Leverages [`sbitmedia.monit`](https://github.com/sbitmedia/ansible-monit) and
[`sbitmedia.munin`](https://github.com/sbitmedia/ansible-munin) roles when
available.

For in-depth explanation of action plugins in roles please see
[sbitmedia.monit's README](https://github.com/sbitmedia/ansible-monit/blob/master/README.md).


Requirements
------------

Since Ansible doesn't support action plugins in roles, it is needed to
explicitly add the path to this role's action plugins in [`ansible.cfg`](https://github.com/ansible/ansible/blob/devel/examples/ansible.cfg).

Example:

```ini
action_plugins     = ./contrib/roles/sbitmedia.monit/action_plugins
                    :./contrib/roles/sbitmedia.munin/action_plugins
                    :./contrib/roles/sbitmedia.fail2ban/action_plugins
```

Happily, action_plugins supports relative paths. Paths are separated by colon
(`:`).


Role Variables
--------------

Default variables are documented in [`defaults/main.yml`](defaults/main.yml).

Role variables are set per OS. See: [`vars/*.yml`](vars/).

See also the args accepted by `fail2ban_jail` in [`library/fail2ban_jail`](library/fail2ban_jail).


Example Usage
-------------

Using the role is straightforward, just include it and set overrides as needed.

Following playbook shows several examples of `fail2ban_jail` usage.

```yaml
- hosts: servers
  roles:
    - sbitmedia.fail2ban

  tasks:
    # Define a jail.
    - fail2ban_jail:
      args:
        name: ssh-test-jail
        enabled: true
        filter: sshd
        port: ssh
        logpath: /var/log/secure
        maxretry: 3
        bantime: 3600

    # Enable a jail defined in jail.conf but disabled.
    - fail2ban_jail:
      args:
        name: ssh-tcpwrapper
        enabled: true
```

Leverage Fail2ban in your roles
-------------------------------

There's two ways to leverage this role in your own roles.

 * Hard dependency: add `sbitmedia.fail2ban` as a dependency in your role and
start ruling your own checks with no drawbacks at all.

 * Soft dependency: use `sbitmedia.fail2ban` when it is available. For this to
work, several thing need to happen:
1. the role must be included before yours.
1. calls to `fail2ban` must be done this way, to avoid syntax errors in
Ansible:

```yaml
- name: Configure fail2ban service in Munin
  action: fail2ban_jail
  args:
    name: ssh
    enabled: true
  when: fail2ban_service is defined
```

License
-------

BSD

Author Information
------------------

Jonathan Araña Cruz - SB IT Media, S.L.

