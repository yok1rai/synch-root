# sync-root

Safely sets up and enters a chroot environment by bind-mounting essential Linux directories.

## Table of Contents

[Description](#description)

[Features](#features)

[Installation](#installation)

[Usage](#usage)

[Folder Structure](#folder-structure)

[How do program actually works](#how-the-program-actual-works)

[LICENSE](#license)

---

## Description

`sync-root` is a small, safe shell utility that automatically bind-mounts essential directories (`/proc`, `/sys`, `/dev`, `/run`, etc.) and then `chroot`s into a target Linux environment.

## Features

- Safe `chroot` setup with automatic bind-mounts.
- Python installer for easy setup to `/usr/local/bin`.

---

## Installation

### Using Python installer (recommended)

#### Dependencies

- `python3` : to run Python scripts

#### Privilege level

`root` : to install the app globally

#### How to install

```bash
sudo python3 install.py
```

### Manual Installation (not recommended)

- Make the `bin/sync-root` executable

```bash
chmod +x ./bin/sync-root
```

- copy or move the `bin/sync-root` to the `/usr/local/bin` to run it anywhere

```bash
# to copy
cp ./bin/sync-root /usr/local/bin/

# to move
mv ./bin/sync-root /usr/local/bin/
```

---

## Usage

```bash
# basic usage
sudo sync-root /path/to/target

# Example
sudo sync-root ~/minimal-linux
```

### Arguments

1. argument (required) : Path of the target Linux OS
2. argument (optional) : Path of the initial shell in the target OS. By default, it's `/bin/bash`

1. flag (`-f`)     : skip bind-mounting `/etc/resolv.conf` if needed

```bash
# usage with only required arguments
sudo sync-root ~/minimal-linux

# usage with second argument too
sudo sync-root ~/minimal-linux /bin/zsh

# usage wit -f flag
sudo sync-root ~/minimal-linux -f

# usage with all arguments
sudo sync-root ~/minimal-linux /bin/zsh -f
```

⚠️ Note:

If you want to use the third argument while keeping the default shell,
you must explicitly pass `/bin/bash` as the second argument.


### Errors

### Prerequisite Errors (code 1)

1. First argument is empty
2. Directory given for the first argument does not exist
3. Target directory is in the live root filesystem
4. Executable shell not found
5. Program didn’t run with root privileges

### Binding Errors (code 2)

1. /proc not found
2. /sys not found
3. /dev not found
4. /dev/pts not found
5. /dev/shm not found
6. /run not found
7. /etc/resolv.conf not found

### Invalid Argument (code 3)

1. Wrong value given for the third positional argument

---

## Folder Structure

```bash
sync-root
├── bin/
│   └── sync-root # source file
├── changelog.md  # Change Logs
└── install.py    # automatic installation script, written in Python
```
---

## How the program actual works

sync-root is a small Bash utility that prepares a target directory to behave like a real Linux root filesystem and then enters it using chroot

In short:

**it bind-mounts the required kernel and system interfaces into the target root and then chroots into it.**


⚠️ Safety note: While basic checks are performed, this is **not a sandbox**. You are effectively interacting with the host kernel.

### Program Flow

The program runs in **three stages:**

1. **Prerequisite checks**
2. **Bind-mount required system directories**
3. **Change root and spawn a shell**

#### Stage 1 — Prerequisite checks

Before touching anything, the script validates the environment:

- Ensures a **target directory** is provided
- Ensures the target exists and **is a directory**
- Prevents `chroot`'ing into the **Live root filesystem (`/`)**
- Verifies that a **shell exists inside the target (default: /bin/bash)**
- Ensures the script is run as **root**

If any of these checks fail, execution stops immediately to avoid damage.

#### Stage 2 — Binding required system directories

To make the chroot usable, several virtual and runtime filesystems from the host must be available inside the target.

The script creates mount points inside the target and then mounts:

| Host Path  | Purpose                        |
| :--------- | :----------------------------- |
| `/proc`    | Process and kernel info        |
| `/sys`     | Hardware and kernel interfaces |
| `/dev`     | Device nodes                   |
| `/dev/pts` | Pseudo-terminals               |
| `/dev/shm` | Shared memory                  |
| `/run`     | Runtime system state           |

Most mounts use `--rbind` to ensure submounts are included.

#### DNS handling (/etc/resolv.conf)

By default, the script copies `/etc/resolv.conf` into the target so networking works inside the chroot.

You can skip this step by passing `f` as the third argument:

```bash
sync-root /path/to/root /bin/bash f
```

Skipping it may result in **no internet access** inside the chroot.

#### Stage 3 — Changing the root

Once everything is mounted:

```bash
chroot "$target" "$shell"
```

This replaces `/` with the target directory and launches the specified shell.

At this point:

- You are inside the chroot
- The kernel is still the **host’s kernel**
- Mounted resources remain active until manually unmounted

---

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit "https://opensource.org/license/mit")
