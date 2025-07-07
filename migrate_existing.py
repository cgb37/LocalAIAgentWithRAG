"""
Migration script to convert existing data to new project structure
"""
import os
import shutil
from pathlib import Path


def migrate_existing_data():
    """Migrate existing data to new project structure"""
    
    # Create projects directory
    projects_dir = Path("./projects")
    projects_dir.mkdir(exist_ok=True)
    
    # Migrate UX Maturity project
    print("Creating UX Maturity project...")
    ux_dir = projects_dir / "ux_maturity"
    ux_dir.mkdir(exist_ok=True)
    
    if os.path.exists("uxmaturity2018_dataset_redacted.csv"):
        shutil.copy("uxmaturity2018_dataset_redacted.csv", ux_dir / "data.csv")
        print("✓ Copied UX Maturity data")
    
    # Migrate LCSH project
    print("Creating LCSH Variant Labels project...")
    lcsh_dir = projects_dir / "lcsh_variant_labels"
    lcsh_dir.mkdir(exist_ok=True)
    
    if os.path.exists("lcsh_variant_labels.csv"):
        shutil.copy("lcsh_variant_labels.csv", lcsh_dir / "data.csv")
        print("✓ Copied LCSH data")
    
    # Create restaurant reviews project if CSV exists
    if os.path.exists("realistic_restaurant_reviews.csv"):
        print("Creating Restaurant Reviews project...")
        restaurant_dir = projects_dir / "restaurant_reviews"
        restaurant_dir.mkdir(exist_ok=True)
        shutil.copy("realistic_restaurant_reviews.csv", restaurant_dir / "data.csv")
        print("✓ Copied Restaurant Reviews data")
    
    print("\nMigration completed!")
    print("Project directories created:")
    for project in projects_dir.iterdir():
        if project.is_dir():
            print(f"  - {project.name}")
    
    print("\nNext steps:")
    print("1. Run create_project_files.py to generate project.py and prompt.txt files")
    print("2. Test the new system with: python3 new_main.py")


if __name__ == "__main__":
    migrate_existing_data()
