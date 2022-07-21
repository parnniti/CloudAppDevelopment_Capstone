/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const COUCH_URL = "https://db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix.cloudantnosqldb.appdomain.cloud";
const IAM_API_KEY = "zRYGmwl5fu4dP_NVCvUd4Vc8lyiBphX4CjSf5bwXvfvr"


async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(COUCH_URL);
    try {
        const dbName = "dealerships"
        if (params.state) {
            let found = await cloudant.postFind({
                db: dbName,
                selector: {st: params.state},
            });
            return found.result.docs;

        } else {
            let db = await cloudant.postAllDocs({
                db: dbName,
                includeDocs: true,
            });
            let all_dealerships = []
            db.result.rows.map(function(e) {
                all_dealerships.push(e.doc);
            });
            console.log(all_dealerships);
            return all_dealerships;
        };
            
    } catch (error) {
        return { error: error.description };
    };
};