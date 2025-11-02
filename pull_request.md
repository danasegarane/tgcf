# Pull Request Title
web(ui): add config import to Advanced page; ci: add Docker build/push workflow

# Pull Request Body
Add import flow to Advanced page so authorized users can upload a tgcf JSON config, validate it with the pydantic Config model and persist via write_config (supports file or Mongo storage). Also add a GitHub Actions workflow to build and push the Docker image to GHCR when changes are merged to main.

## Changes:
- tgcf/web_ui/pages/6_🔬_Advanced.py — add Import config UI, validation and persistence
- .github/workflows/docker-build.yml — build & push Docker image to GHCR (add this file)

## Notes:
- The import flow replaces the config by validating the uploaded JSON against the Config model. If you prefer merging partial configs instead, we can change the import behavior.
- The workflow pushes to GHCR (ghcr.io). If you want Docker Hub instead, let me know so I can adapt the workflow.
- Ensure repository permissions allow workflow to push to GHCR (packages: write). Using the default GITHUB_TOKEN usually works but check your repo settings if you get permission errors.