{
  description = "wpressarc - Convert ai1wm wpress archives to and from tar archives";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-parts.url = "github:hercules-ci/flake-parts";
  inputs.devshell.url = "github:numtide/devshell";
  inputs.flake-compat.url = "https://flakehub.com/f/edolstra/flake-compat/1.tar.gz";

  outputs = inputs @ {
    nixpkgs,
    flake-parts,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = [
        "i686-linux"
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      imports = [inputs.devshell.flakeModule];
      perSystem = {
        pkgs,
        config,
        ...
      }: {
        packages = {
          wpressarc = pkgs.callPackage ./package.nix {inherit pkgs;};
          default = config.packages.wpressarc;
        };
        apps = {
          wpressarc = {
            type = "app";
            program = "${config.packages.wpressarc}/bin/wpressarc";
          };
          default = config.apps.wpressarc;
        };
        devshells.default = {
          packages = with pkgs; [python3];
        };
      };
    };
}
