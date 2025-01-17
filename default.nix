let
    pkgs = (import (builtins.fetchTarball {
        name="nixos_stable_23.11_20240406";
        url = "https://github.com/NixOS/nixpkgs/archive/e38d7cb66ea4f7a0eb6681920615dfcc30fc2920.tar.gz";
        sha256 = "1shml3mf52smfra0x3mpfixddr4krp3n78fc2sv07ghiphn22k43";
    }) { });
    stdenv = pkgs.stdenv;

in pkgs.mkShell rec {
    name = "nix-shell";
    shellHook = ''
        source .bashrc
    '';
    buildInputs = (with pkgs; [
        bashInteractive
        (pkgs.python3.buildEnv.override {
            ignoreCollisions = true;
            extraLibs = with pkgs.python3.pkgs; [
                beautifulsoup4
                lxml
                pprintpp
                python-dotenv
                requests
                selenium
            ];
        })
    ]);
}

