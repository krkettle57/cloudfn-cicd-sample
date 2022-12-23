# Github Actions で始める Cloud Functions

- 前提条件
  - Google Cloud のアカウント作成
  - `gcloud`のインストール
- 動作検証環境
  - Python: 3.9.10
  - Docker: 20.10.12
  - act: 0.2.34

## 実行手順

この章では以下の手順を示します

- Google Cloud 環境の作成
- (省略可) ローカル検証環境の構築
- (省略可) Google Cloud 環境の削除

### Google Cloud 環境の作成

1. 環境変数の定義

```shell
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_NAME="cloudfn-cicd-sample"
REPO="krkettle57/cloudfn-cicd-sample"
GCS_BUCKET="${PROJECT_ID}-cloudfn-cicd-sample"
```

2. Workload Identity の作成

```shell
gcloud iam workload-identity-pools create "sample-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="sample pool"
gcloud iam workload-identity-pools providers create-oidc "sample-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="sample-pool"\
  --display-name="sample provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

3. サービスアカウントの作成及び権限の付与

```shell
WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe sample-pool \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"
)
WORKLOAD_IDENTITY_PROVIDER_ID=$(gcloud iam workload-identity-pools providers describe sample-provider \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="sample-pool" \
  --format="value(name)"
)
SERVICE_ACCOUNT_ID="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME --display-name="Cloud Functions CICD sample service account"
gcloud iam service-accounts add-iam-policy-binding "${PROJECT_ID}@appspot.gserviceaccount.com" \
  --member "serviceAccount:${SERVICE_ACCOUNT_ID}" \
  --role roles/iam.serviceAccountUser
gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT_ID \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${REPO}"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --role="roles/cloudfunctions.developer" \
  --member="serviceAccount:${SERVICE_ACCOUNT_ID}"
```

4. サービスの有効化

```shell
gcloud services enable iamcredentials.googleapis.com \
  --project "${PROJECT_ID}"
gcloud services enable cloudfunctions.googleapis.com \
  --project "${PROJECT_ID}"
gcloud services enable cloudbuild.googleapis.com \
  --project "${PROJECT_ID}"
```

5. 設定値の出力

以下で実行した内容を、github/workflows/run.yml の `CHANGE ME`の部分に反映させます

```shell
echo "WORKLOAD_IDENTITY_PROVIDER: ${WORKLOAD_IDENTITY_PROVIDER_ID}"
echo "DEPLOY_SERVICE_ACCOUNT: ${SERVICE_ACCOUNT_ID}"
```

### (省略可) ローカル検証環境の構築

1. 各種ツールのインストール

- [Docker](https://docs.docker.com/)
- [act](https://github.com/nektos/act)

2. ビルド用 Docker イメージを作成

```shell
docker build -t ubuntu-builder .
```

3. ローカルで Github Actions の検証

```shell
act \
  -P ubuntu-latest=ubuntu-builder \
  -e .github/workflows/event.json \
  --artifact-server-path /tmp/act-artifacts
```

### (省略可) Google Cloud 環境の削除

```shell
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_NAME="cloudfn-cicd-sample"
GITHUB_USER="krkettle57"
GITHUB_REPO="cloudfn-cicd-sample"
GCS_BUCKET="${PROJECT_ID}-cloudfn-cicd-sample"
WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe sample-pool \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)")
SERVICE_ACCOUNT_ID="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud -q iam service-accounts delete $SERVICE_ACCOUNT_ID
gcloud -q iam workload-identity-pools delete $WORKLOAD_IDENTITY_POOL_ID \
  --location="global"
```

## 検証中に起きた課題

### act で cache が有効にならない

- poetry のインストール結果をキャッシュとして保持するように設定しているが、act 上では`cache=false`となり、毎回インストールが実行される
- GitHub Actions 上ではキャッシュが有効になり、2 回目以降のインストールはスキップされる

### gsutil コマンドで 401 エラーが発生する

- `gsutil`
- [Issue](https://github.com/google-github-actions/auth/issues/241#issuecomment-1309540404)を参考に`google-github-actions/auth@v1`の後に`gcloud -q auth login --cred-file="$GOOGLE_APPLICATION_CREDENTIALS"`を実行すると解消した
- ※現在は`gsutil`コマンドを使っていない
