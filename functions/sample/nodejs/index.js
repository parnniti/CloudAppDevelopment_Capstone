/**
 * Get all databases
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const params = {
    "COUCH_URL": "https://db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "zRYGmwl5fu4dP_NVCvUd4Vc8lyiBphX4CjSf5bwXvfvr",
    "COUCH_USERNAME": "db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix",
}

function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbList = getDbs(cloudant);
    return { dbs: dbList };
}

function getDbs(cloudant) {
    cloudant.getAllDbs().then((body) => {
        body.forEach((db) => {
            dbList.push(db);
        });
    }).catch((err) => { console.log(err); });
}