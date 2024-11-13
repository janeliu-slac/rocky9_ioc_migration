# Git fork all IOC repos

# Git fork repos that start with "ioc"
gh repo list pcdshub --limit 2000 | while read -r repo _; do
  if [[ $repo == pcdshub/ioc* ]] ;
  then
    gh repo fork "$repo" --default-branch-only --remote
  fi
done