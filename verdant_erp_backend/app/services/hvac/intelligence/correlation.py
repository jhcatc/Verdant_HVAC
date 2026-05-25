from sqlalchemy import text


async def customer_failure_correlation(db):

    result = await db.execute(text("""
        SELECT
            c.name AS customer,
            COUNT(so.id) AS total_orders,
            SUM(CASE WHEN so.status = 'failed' THEN 1 ELSE 0 END) AS failed_orders
        FROM service_orders so
        JOIN customers c ON c.id = so.customer_id
        GROUP BY c.name
    """))

    rows = result.fetchall()

    output = []

    for r in rows:

        failure_rate = (r.failed_orders / r.total_orders) * 100 if r.total_orders else 0

        output.append({
            "customer": r.customer,
            "total_orders": r.total_orders,
            "failed_orders": r.failed_orders,
            "failure_rate": round(failure_rate, 2),
            "insight": f"{r.customer} tiene {round(failure_rate,2)}% de fallas"
        })

    return sorted(output, key=lambda x: x["failure_rate"], reverse=True)