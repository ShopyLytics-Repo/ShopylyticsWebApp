# Build and deploy

Command to build the application. PLease remeber to change the project name and application name
```
gcloud builds submit --tag gcr.io/shopylytics-irt-demo/shopylytics-irt-demo-app  --project=shopylytics-irt-demo
```

Command to deploy the application
```
gcloud run deploy --image gcr.io/shopylytics-irt-demo/shopylytics-irt-demo-app --platform managed  --project=shopylytics-irt-demo --allow-unauthenticated
```