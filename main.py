import flask
from google.cloud import bigquery


app = flask.Flask(__name__)
bigquery_client = bigquery.Client()


@app.route("/")
def main():
    query_job = bigquery_client.query(
        """
        #standardSQL
        SELECT *
        FROM ml.PREDICT(
            MODEL `msds-434-analytics-app.house_analytics`.house_price_model2,
        (

        #standardSQL
        WITH params AS (
            SELECT
            1 AS TRAIN,
            2 AS EVAL
            ),

        house_sales AS (
        SELECT
            bedrooms,
            bathrooms,
            sqft_living,
            sqft_lot,
            waterfront,
            condition,
            grade,
            yr_built,
            zipcode,
            price
        FROM
            `msds-434-analytics-app.house_analytics.kc_house_data_clean`,
            params
        WHERE
            price > 0 AND bedrooms < 6
            AND MOD(ABS(FARM_FINGERPRINT(
                CAST(id AS STRING))),1000) = params.EVAL
        )


        SELECT *
        FROM house_sales
        ))
        """
    )

    return flask.redirect(
        flask.url_for(
            "query_results",
            project_id=query_job.project,
            job_id=query_job.job_id,
            location=query_job.location,
        )
    )


@app.route("/query_results")
def query_results():
    project_id = flask.request.args.get("project_id")
    job_id = flask.request.args.get("job_id")
    location = flask.request.args.get("location")

    query_job = bigquery_client.get_job(
        job_id,
        project=project_id,
        location=location,
    )

    results = query_job.result(timeout=30)

    return flask.render_template("query_result.html", results=results)


if __name__ == "__main__":

    app.run(host="127.0.0.1", port=8080, debug=True)
