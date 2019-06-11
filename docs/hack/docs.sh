# Exit at first error
set -e

# Clear sphinx-apidoc output directory
rm -rf docs/source/apidoc/*
# Execute sphinx-apidoc
sphinx-apidoc -f -e -o docs/source/apidoc/ final_project_squad5/
# Clear build directory
rm -rf docs/build/*
# Copy md files from docs to source/md folder
mkdir -p docs/source/md/
cp docs/*.md docs/source/md/
# Change file to show "API" in the table of contents rather than the package's name
sed -i '0,/final_project_squad5/s//API/' docs/source/apidoc/modules.rst
# Show package's name in the home page
sed -i '0,/project/s//final_project_squad5/' docs/source/index.rst
# Generate html docs
make -C docs/ html
# Clear temp files at source/md directory
rm -rf docs/source/md/*
