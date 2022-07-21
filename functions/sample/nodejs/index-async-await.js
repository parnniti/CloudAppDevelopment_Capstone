/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
const params = {
    "COUCH_URL": "https://db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "zRYGmwl5fu4dP_NVCvUd4Vc8lyiBphX4CjSf5bwXvfvr",
    "COUCH_USERNAME": "db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix",
}

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let dbList = await cloudant.getAllDbs();
        let db = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
        });
        let all_dealerships = []
        db.result.rows.map(function(e) {
            all_dealerships.push(e.doc)
        });

        console.log(all_dealerships)

        return { "dbs": dbList.result };
    } catch (error) {
        return { error: error.description };
    }
}

main(params)


