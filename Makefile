.PHONY: release help

MARKETPLACE_JSON := .claude-plugin/marketplace.json

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  release   Create a new release (bump version, commit, tag, push)"
	@echo "  help      Show this help"

release:
	@# Check for uncommitted changes
	@if ! git diff --quiet || ! git diff --cached --quiet; then \
		echo "Error: You have uncommitted changes. Please commit or stash them first."; \
		git status --short; \
		exit 1; \
	fi
	@echo ""
	@current=$$(grep '"version"' $(MARKETPLACE_JSON) | sed 's/.*"version": *"\([^"]*\)".*/\1/'); \
	echo "Current version: $$current"; \
	echo ""; \
	major=$$(echo $$current | cut -d. -f1); \
	minor=$$(echo $$current | cut -d. -f2); \
	patch=$$(echo $$current | cut -d. -f3); \
	next_patch="$$major.$$minor.$$((patch + 1))"; \
	next_minor="$$major.$$((minor + 1)).0"; \
	echo "Suggested versions:"; \
	echo "  [enter] patch: $$next_patch (bug fixes, small changes)"; \
	echo "  [m]     minor: $$next_minor (new features)"; \
	echo ""; \
	read -p "New version [$$next_patch]: " input; \
	if [ -z "$$input" ]; then \
		new_version="$$next_patch"; \
	elif [ "$$input" = "m" ] || [ "$$input" = "M" ]; then \
		new_version="$$next_minor"; \
	else \
		new_version="$$input"; \
	fi; \
	echo ""; \
	echo "Updating version to $$new_version..."; \
	sed -i '' 's/"version": "[^"]*"/"version": "'$$new_version'"/' $(MARKETPLACE_JSON); \
	echo "Updated $(MARKETPLACE_JSON)"; \
	echo ""; \
	git add $(MARKETPLACE_JSON); \
	git commit -m "Release v$$new_version"; \
	git tag -a "v$$new_version" -m "Release v$$new_version"; \
	echo ""; \
	echo "Pushing to remote..."; \
	git push && git push --tags; \
	echo ""; \
	echo "✓ Released v$$new_version"
