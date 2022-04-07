#!/usr/bin/env python3

import gzip
import platform
import shutil
import stat
import subprocess
import sys
import os

def UnsupportedPlatformError(Exception):
    def __init__(self, details):
        self.message = "error: rust-analyzer is unavailable for {}".format(details)

def normalize_arch(arch):
    if arch == "arm64":
        return "aarch64"
    return arch

def abi_for_os(os, libc):
    if os == "Linux":
        return "unknown-linux-" + libc
    elif os == "macOS":
        return "apple-darwin"
    assert(os == "Windows")
    # Assuming the MSVC ABI ¯\_(ツ)_/¯
    return "pc-windows-msvc"

RUNNER_OS = os.environ['RUNNER_OS']

def rust_analyzer_archive_url():
    RUNNER_ARCH = normalize_arch(platform.machine())
    libc = None

    # The supported combinations here are based on the rust-analyzer binaries
    # available:
    # https://github.com/rust-analyzer/rust-analyzer/releases/tag/2021-11-01
    if RUNNER_OS == "Linux":
        process_result = subprocess.run(["/usr/bin/ldd", "--version"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
        version_output = process_result.stdout.decode("utf-8").lower()
        # musl-ldd doesn't actually support --version according to
        # https://manpages.debian.org/stretch/musl-tools/musl-ldd.1
        # so the call above may fail, but the output still has "musl"
        if "musl" in version_output:
            if RUNNER_ARCH != "x86_64":
                raise UnsupportedPlatformError("arch + libc ({} + musl)".format(RUNNER_ARCH))
            libc = "musl"
        elif "glibc" in version_output or "gnu" in version_output:
            if RUNNER_ARCH != "x86_64" and RUNNER_ARCH != "aarch64":
                raise UnsupportedPlatformError("arch + libc ({} + gnu)".format(RUNNER_ARCH))
            libc = "gnu"
        else:
            raise UnsupportedPlatformError("libc (not gnu or musl?)")
    elif RUNNER_OS == "macOS" or RUNNER_OS == "Windows":
        if RUNNER_ARCH != "x86_64" and RUNNER_ARCH != "aarch64":
            raise UnsupportedPlatformError("arch + OS ({} + Windows)".format(RUNNER_ARCH))
    else:
        raise UnsupportedPlatformError("OS ({})".format(RUNNER_OS))

    ABI = abi_for_os(RUNNER_OS, libc)
    RUST_ANALYZER_ARCHIVE = ("rust-analyzer-{}-{}.gz".format(RUNNER_ARCH, ABI))
    RUST_ANALYZER_RELEASE = "2022-03-21"
    return ("https://github.com/rust-analyzer/rust-analyzer/releases/download/{}/{}"
            .format(RUST_ANALYZER_RELEASE, RUST_ANALYZER_ARCHIVE))

def setup_rust_analyzer():
    curl_result = subprocess.run(["curl", "-sfL", rust_analyzer_archive_url(), "--output", "rust-analyzer.gz"])
    curl_result.check_returncode()
    if RUNNER_OS == "Windows":
        RUST_ANALYZER_FILE_NAME = "rust-analyzer.exe"
    else:
        RUST_ANALYZER_FILE_NAME = "rust-analyzer"
    with gzip.open("rust-analyzer.gz", 'r') as f_in, open(RUST_ANALYZER_FILE_NAME, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    current_perms = os.stat(RUST_ANALYZER_FILE_NAME)
    os.chmod(RUST_ANALYZER_FILE_NAME, current_perms.st_mode | stat.S_IEXEC)

setup_rust_analyzer()
