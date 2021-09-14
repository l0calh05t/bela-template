# `bela-template`

This project is a [`cargo-generate`](https://github.com/cargo-generate/cargo-generate/) template for building [Bela](https://bela.io) projects using Rust and [the `next` branch of `l0calh05t/bela-rs`](https://github.com/l0calh05t/bela-rs/tree/next) (a fork of [`andrewcsmith/bela-rs`](https://github.com/andrewcsmith/bela-rs/)).

## Initial Setup

1. Install `cargo-generate` by running

   ```bash
   cargo install cargo-generate
   ```

2. [Download a Bela image](https://github.com/BelaPlatform/bela-image-builder/releases/), matching the image on your Bela.
   This code was tested with Bela 0.3.8b

3. Extract the Bela image's root file system to a folder of your choice.
   For example, using [7-Zip](https://www.7-zip.org/) on Windows, this can be achieved by opening the `.img.xz`-File as an archive, opening the `.img` within as an archive, then extracting the contents of `1.img` (the largest partition) within to a folder of your choice.

4. Set the `BELA_SYSROOT` environment variable to the folder you extracted the image to.
   If you set it in a permanent place, such as `.profile` on Linux or the Windows Registry, you only have to do this once.
   Otherwise, remember to set it for every new shell/application you want to run `cargo build` etc. in.

   > If you use [Visual Studio Code](https://code.visualstudio.com/) with the [rust-analyzer Plugin](https://rust-analyzer.github.io/) *and* haven't set the variable permanently, I recommend adding a `.vscode/settings.json` containing
   >
   > ```json
   > {
   >     "rust-analyzer.server.extraEnv": {
   >         "BELA_SYSROOT": "<PATH_TO_EXTRACTED_IMAGE>"
   >     }
   > }
   > ```
   >
   > to your Bela projects.
5. Install a compatible ARM GCC cross-compiler tool chain and add it to your `PATH`.
   Compatible toolchains include
   - [The old GCC 7.5 Linaro tool chain](https://releases.linaro.org/components/toolchain/binaries/7.5-2019.12/arm-linux-gnueabihf/)
   - [The current GCC 10.*x* official ARM tool chain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads)
   - [Bela's own macOS tool chain](http://files.bela.io/gcc/)

   > Depending on the tool chain of your choice, you may have to adapt the `linker` setting in `.cargo/config.toml` later on.
6. In addition to Rust, you will require
   - a Python 3.6+ interpreter (accessible via your `PATH` under the name `python`),
   - the OpenSSL `ssh` client (should already be installed on most systems), and
   - the `rsync` client.

   > Windows users: install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10), since `runner.py` uses `wsl rsync`.

## Usage

To create a new Bela project, run

```bash
cargo generate --git https://github.com/l0calh05t/bela-template.git --name my-project
cd my-project
```

Then proceed with building using `cargo build` etc. as usual.
To run tests (`cargo test`), benchmarks (`cargo bench`), or your new application (`cargo run` — since the Bela is very resource-constrained, you should typically add the `--release` flag), the Bela must be connected to your computer and available via the `bela.local` DNS name and have password-less root login enabled (both these settings are the default), so that the runner-script `runner.py` can access the Bela.

For further usage examples, check out [the `examples`-folder in `bela-rs`](https://github.com/l0calh05t/bela-rs/tree/next/examples) (this template is based on `examples/hello.rs`).

## License

The template is licensed under the [MIT license](LICENSE-MIT) OR the [Apache License Version 2.0](LICENSE-APACHE).
The `license` field has been omitted in `Cargo.toml` as projects based on this template can use any compatible license.
