import argparse
import sys
from pathlib import Path

from depscripter.scanner import scan_imports
from depscripter.resolver import resolve_packages
from depscripter.injector import generate_script_metadata, inject_metadata

def main():
    parser = argparse.ArgumentParser(description="Add PEP 723 metadata to Python scripts.")
    parser.add_argument("file", type=Path, help="Path to the Python script")
    parser.add_argument("--no-pin", action="store_true", help="Do not pin package versions")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--in-place", action="store_true", help="Modify the file in-place")
    group.add_argument("-o", "--output", type=Path, help="Write output to a specific file")
    
    args = parser.parse_args()
    
    if not args.file.exists():
        sys.exit(f"Error: File {args.file} not found.")
        
    source_code = args.file.read_text(encoding="utf-8")
    
    # Scan
    modules = scan_imports(source_code)
    
    # Resolve
    dependencies = resolve_packages(modules, pin_versions=not args.no_pin)
    
    # Generate metadata
    metadata = generate_script_metadata(dependencies)
    
    # Inject
    new_source = inject_metadata(source_code, metadata)
    
    if args.in_place:
        args.file.write_text(new_source, encoding="utf-8")
        print(f"Updated {args.file}")
    elif args.output:
        args.output.write_text(new_source, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        print(new_source, end="")

if __name__ == "__main__":
    main()
