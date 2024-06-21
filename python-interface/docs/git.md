
## Setup

```
git config --global core.editor "nano"
git push --set-upstream origin new-branch
git remote add upstream https://github.com/XXXX.git
```


## Info
```
git log --oneline --graph --all
git remote -v
git diff jeffrey/pr2 origin/main

```

## Update:
```
git fetch upstream
git merge upstream/main
git pull upstream main
git push origin your-feature-branch
```

## Modify
```
git branch -d BRANCH_NAME
git push ORIGIN --delete BRANCH_NAME
```
### Delete last commit 
Delete locally
```
git reset --hard HEAD~1
```
then delete form remote as well
```
git push jeffrey main --force
```

# How to create pull request into remote branch??
This opens a pull request in my fork:
```
gh pr create --assignee '@me' --head pr2 --base main --body "test" --title "test" 
```
This does not wok:
```
gh pr create --assignee '@me' --head pr2 --base main --body "test" --title "test" 
```
gives:
```
pull request create failed: GraphQL: Head sha can't be blank, Base sha can't be blank, No commits between origin/main and origin/pr2, Head ref must be a branch, Base ref must be a branch (createPullRequest)

```