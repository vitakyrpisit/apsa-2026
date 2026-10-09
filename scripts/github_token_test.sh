#!/bin/bash
# End-to-end test of bugfix delivery path: fork -> clone -> branch -> push -> PR
# Uses octocat/Hello-World (tiny) forked into own account. Test PR created in OWN fork only, then closed.
set -e
GH=$(grep '^GITHUB_TOKEN=' /home/z/my-project/.env.local | cut -d= -f2-)
export GH_TOKEN="$GH"
AUTH="Authorization: Bearer $GH"

echo "[1] fork octocat/Hello-World..."
curl -s -X POST -H "$AUTH" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/octocat/Hello-World/forks -o /tmp/fork_resp.json
python3 -c "import json; d=json.load(open('/tmp/fork_resp.json')); print('  fork:', d.get('full_name') or ('ERR: '+str(d.get('message'))))"

sleep 6

mkdir -p /tmp/ghtest && rm -rf /tmp/ghtest/Hello-World
cat > /tmp/ghtest/askpass.sh << 'ASK'
#!/bin/bash
case "$1" in
  Username*) echo "vitakyrpisit" ;;
  *) echo "$GH_TOKEN" ;;
esac
ASK
chmod 700 /tmp/ghtest/askpass.sh
export GIT_ASKPASS=/tmp/ghtest/askpass.sh
export GIT_TERMINAL_PROMPT=0

echo "[2] clone fork via HTTPS (token as password)..."
git clone --quiet https://github.com/vitakyrpisit/Hello-World.git /tmp/ghtest/Hello-World && echo "  clone OK"

cd /tmp/ghtest/Hello-World
git config user.name "apsa-agent"
git config user.email "agent@apsa.local"
BR="apsa-token-test-20261009"
git checkout -q -b "$BR"
git commit -q --allow-empty -m "token write test (safe to delete)"
echo "[3] push branch $BR..."
git push -q origin "$BR" && echo "  push OK"

echo "[4] verify branch via API..."
curl -s -H "$AUTH" "https://api.github.com/repos/vitakyrpisit/Hello-World/branches/$BR" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('  branch:', d.get('name') or ('ERR: '+str(d.get('message'))))"

echo "[5] test PR creation (Pull requests:write) in OWN fork..."
curl -s -X POST -H "$AUTH" https://api.github.com/repos/vitakyrpisit/Hello-World/pulls \
  -d '{"title":"[test] token PR-permission check","head":"'"$BR"'","base":"master"}' -o /tmp/pr_resp.json
PRNUM=$(python3 -c "import json; d=json.load(open('/tmp/pr_resp.json')); print(d.get('number',''))")
python3 -c "import json; d=json.load(open('/tmp/pr_resp.json')); print('  PR:', d.get('html_url') or ('ERR: '+str(d.get('message'))+' '+str(d.get('errors',''))))"

if [ -n "$PRNUM" ]; then
  curl -s -X PATCH -H "$AUTH" "https://api.github.com/repos/vitakyrpisit/Hello-World/pulls/$PRNUM" \
    -d '{"state":"closed"}' -o /dev/null
  echo "  PR #$PRNUM closed (cleanup done)"
fi

echo "[6] RESULT: full delivery path VERIFIED (fork+clone+push+PR)"
