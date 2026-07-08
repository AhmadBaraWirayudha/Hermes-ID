extern "C" {
void moving_average(const double* input, int n, int window, double* output) {
    if (window < 1) window = 1;
    double sum = 0.0;
    for (int i = 0; i < n; ++i) {
        sum += input[i];
        if (i >= window) sum -= input[i - window];
        int denom = (i + 1 < window) ? (i + 1) : window;
        output[i] = sum / denom;
    }
}

double elasticity(double pct_delta_q, double pct_delta_p) {
    if (pct_delta_p == 0.0) return 0.0;
    return pct_delta_q / pct_delta_p;
}
}
