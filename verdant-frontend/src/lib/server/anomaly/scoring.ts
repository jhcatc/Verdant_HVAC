export function calculateEfficiencyScore(order: any) {
    const estimated = order.estimated_hours || 1;
    const actual = order.actual_hours || 1;

    const ratio = actual / estimated;

    // > 1 = peor performance
    if (ratio <= 1) return 0;

    if (ratio <= 1.3) return 20;
    if (ratio <= 1.6) return 50;

    return 80;
}

export function calculateCostDeviation(order: any) {
    const estimated = order.estimated_cost || 1;
    const actual = order.actual_cost || 1;

    const ratio = actual / estimated;

    if (ratio <= 1) return 0;
    if (ratio <= 1.2) return 30;
    if (ratio <= 1.5) return 60;

    return 90;
}

export function calculateRecurrenceScore(orderCount: number) {
    if (orderCount <= 1) return 0;
    if (orderCount <= 2) return 30;
    if (orderCount <= 3) return 60;
    return 90;
}