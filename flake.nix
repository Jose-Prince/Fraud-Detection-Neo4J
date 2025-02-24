{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let 
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };  
  in {
    devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
            pkgs.dotnet-sdk_8
        ];
        
        shellHook = ''
            echo "Assure Neo4J Driver is installed"
            if [ ! -f "packages.lock.json" ]; then 
                dotnet new console --force
                dotnet add package Neo4J.Driver
                dotnet add package Microsoft.AspNetCore.App
                dotnet add package DotNetEnv
                dotnet add package Swashbuckle.AspNetCore
            fi
        '';
    };
  };
}
