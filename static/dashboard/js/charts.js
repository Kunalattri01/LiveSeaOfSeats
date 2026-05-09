function salesAnalyticsChart() {
  const analyticsCtx = document.getElementById("salesAlalyticsChart");
  if (!analyticsCtx) return;

  // 1. Always get the LATEST colors from CSS variables
  const getCSSVar = (varName) =>
    getComputedStyle(document.documentElement).getPropertyValue(varName).trim();

  const colors = {
    bar: getCSSVar("--blue-deep"),
    text: getCSSVar("--text"),
    muted: getCSSVar("--muted"),
    grid: getCSSVar("--border"),
    card: getCSSVar("--card"),
  };

  // 2. Destroy existing instance to prevent "ghosting" or overlapping
  const existingChart = Chart.getChart(analyticsCtx);
  if (existingChart) {
    existingChart.destroy();
  }

  // Select the active palette

  const salesChart = new Chart(analyticsCtx, {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [
        {
          label: "Sales",
          data: [420, 520, 610, 480, 700, 820],
          backgroundColor: colors.bar, // Using the blue variable
          borderRadius: 10,
          barThickness: 38,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: colors.text, // Using the text variable
            font: { size: 14, weight: "600" },
          },
        },
        tooltip: {
          // You can use logic for your 'isDark' state here
          backgroundColor: colors.text,
          titleColor: colors.card,
          bodyColor: colors.card,
          padding: 12,
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: colors.muted }, // Using muted for axis labels
        },
        y: {
          grid: {
            color: colors.grid, // Using border color for grid lines
            drawBorder: false,
          },
          ticks: { color: colors.muted },
        },
      },
      animation: {
        duration: 1200,
        easing: "easeOutQuart",
      },
    },
  });

  // Re-render on theme toggle
  window.addEventListener("theme-change", () => {
    salesChart.destroy();
    salesAnalyticsChart();
  });
}

let revenueChart = null;
let salesChart = null;

function initCharts() {
  const isDark = document.documentElement.classList.contains("dark");
  const getCSSVar = (varName) =>
    getComputedStyle(document.documentElement).getPropertyValue(varName).trim();

  const colors = {
    bar: getCSSVar("--blue-deep"),
    text: getCSSVar("--text"),
    muted: getCSSVar("--muted"),
    grid: getCSSVar("--border"),
    card: getCSSVar("--card"),
  };

  // Revenue Chart (Doughnut)
  const revenueCtx = document.getElementById("revenue-chart");
  if (revenueCtx) {
    if (revenueChart) revenueChart.destroy(); // destroy previous instance
    revenueChart = new Chart(revenueCtx, {
      type: "doughnut",
      data: {
        labels: ["General", "VIP", "Premium", "Early Bird"],
        datasets: [
          {
            data: [34020, 22250, 20706, 10115],
            backgroundColor: colors.bar,
            borderWidth: 2,
            borderColor: colors.grid,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: colors.text,
              padding: 20,
              usePointStyle: true,
            },
          },
          tooltip: {
            backgroundColor: colors.bar,
            titleColor: colors.text,
            bodyColor: colors.text,
            borderColor: colors.grid,
            borderWidth: 1,
            callbacks: {
              label: function (context) {
                return context.label + ": $" + context.parsed.toLocaleString();
              },
            },
          },
        },
      },
    });
  }

  // Sales Chart (Bar)
  const salesCtx = document.getElementById("sales-chart");
  if (salesCtx) {
    if (salesChart) salesChart.destroy(); // destroy previous instance
    salesChart = new Chart(salesCtx, {
      type: "bar",
      data: {
        labels: ["General", "VIP", "Premium", "Early Bird", "Student"],
        datasets: [
          {
            label: "Tickets Sold",
            data: [756, 178, 234, 289, 142],
            backgroundColor: [
              "rgba(16, 185, 129, 0.8)",
              "rgba(245, 158, 11, 0.8)",
              "rgba(139, 92, 246, 0.8)",
              "rgba(59, 130, 246, 0.8)",
              "rgba(107, 114, 128, 0.8)",
            ],
            borderColor: colors.grid,
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: colors.bar,
            titleColor: colors.text,
            bodyColor: colors.text,
            borderColor: colors.grid,
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            grid: { color: isDark ? "#374151" : "#f3f4f6" },
            ticks: { color: isDark ? "#9ca3af" : "#6b7280" },
          },
          y: {
            grid: { color: isDark ? "#374151" : "#f3f4f6" },
            ticks: { color: isDark ? "#9ca3af" : "#6b7280" },
          },
        },
      },
    });
  }
}


let monthlyBarChartInstance = null;

function initMonthlyBarChart() {
  const canvas = document.getElementById("monthlyBarChart");
  if (!canvas) return;

  // Destroy existing chart before re-creating
  if (monthlyBarChartInstance) {
    monthlyBarChartInstance.destroy();
  }

  monthlyBarChartInstance = new Chart(canvas, {
    type: "bar",
    data: {
      labels: [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
      ],
      datasets: [
        {
          label: "Current",
          data: [60,75,85,50,80,30,55,85,45,75,82,40],
          backgroundColor: "#3b82f6",
          borderRadius: 6,
          categoryPercentage: 0.6,
          barPercentage: 0.5  
        },
        {
          label: "Previous",
          data: [75,85,95,88,90,82,78,92,70,85,98,95],
          backgroundColor: "#d1d5db",
          borderRadius: 6,
          categoryPercentage: 0.6,
          barPercentage: 0.5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          max: 100,
          ticks: {
            callback: value => value + "%"
          },
          grid: {
            color: "rgba(0,0,0,0.05)"
          }
        }
      }
    }
  });
}

let donutChartInstance;

function initDonutChart() {
  const canvas = document.getElementById("donutChart");
  if (!canvas) return;

  if (donutChartInstance) {
    donutChartInstance.destroy();
  }

  // DATA (High / Medium / Low)
  const Organizer = 8734;
  const Attendee = 900;
  const Admin = 366;

  const total = Organizer + Attendee + Admin;

  donutChartInstance = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: ["Organizer", "Attendee", "Admin"],
      datasets: [
        {
          data: [Organizer, Attendee, Admin],
          backgroundColor: [
            "#3b82f6",
            "#8CA9FF",
            "#e5e7eb" 
          ],
          borderWidth: 0,
          cutout: "68%",
          spacing: 2,
          hoverOffset: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: true,
          backgroundColor: "#111827",
          padding: 10,
          cornerRadius: 6,
          titleColor: "#ffffff",
          bodyColor: "#ffffff",
          callbacks: {
            label(context) {
              const value = context.raw;
              const percent = ((value / total) * 100).toFixed(1);
              return `${context.label}: ${value.toLocaleString()} (${percent}%)`;
            }
          }
        }
      },
      animation: {
        animateRotate: true,
        duration: 1200
      }
    },
    plugins: [
      {
        id: "centerText",
        beforeDraw(chart) {
          const { ctx, width, height } = chart;
          ctx.save();

          ctx.font = "600 20px Inter, sans-serif";
          ctx.fillStyle = "#111827";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";

          ctx.fillText(
            total.toLocaleString(),
            width / 2,
            height / 2
          );

          ctx.restore();
        }
      }
    ]
  });
}

let payoutTrendChart;
 function initPayoutTrendChart() {
            const ctx = document.getElementById('payoutTrendChart');
            if (!ctx) return;
            if(payoutTrendChart){
                payoutTrendChart.destroy();
            }
            
            const isDark = document.documentElement.classList.contains('dark');
            const gridColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
            const textColor = isDark ? '#9ca3af' : '#6b7280';
            
            payoutTrendChart=new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: 'Payouts',
                        data: [2850, 3200, 2950, 3650, 3450, 4325],
                        borderColor: '#8b5cf6',
                        backgroundColor: function(context) {
                            const chart = context.chart;
                            const {ctx, chartArea} = chart;
                            if (!chartArea) return;
                            const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                            gradient.addColorStop(0, 'rgba(139, 92, 246, 0)');
                            gradient.addColorStop(1, 'rgba(139, 92, 246, 0.3)');
                            return gradient;
                        },
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: '#8b5cf6',
                        pointBorderColor: isDark ? '#1f2937' : '#ffffff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: isDark ? '#374151' : '#ffffff',
                            titleColor: isDark ? '#ffffff' : '#111827',
                            bodyColor: isDark ? '#d1d5db' : '#4b5563',
                            borderColor: isDark ? '#4b5563' : '#e5e7eb',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return '$' + context.parsed.y.toLocaleString();
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: textColor, font: { size: 11 } }
                        },
                        y: {
                            grid: { color: gridColor },
                            ticks: {
                                color: textColor,
                                font: { size: 11 },
                                callback: function(value) {
                                    return '$' + (value / 1000) + 'k';
                                }
                            }
                        }
                    }
                }
            });
        }

       

// for customar pages
let segmentationChart;
// Initialize segmentation chart
function initSegmentationChart() {
  const segmentationCtx = document.getElementById("segmentation-chart");
  if (!segmentationCtx) return;
  const isDark = document.documentElement.classList.contains("dark");

  if (segmentationChart) segmentationChart.destroy();

  const data = {
    labels: ["VIP", "Gold", "Silver", "Bronze", "Regular"],
    datasets: [
      {
        data: [5.5, 12.3, 23.8, 31.2, 27.2],
        backgroundColor: [
          "#fbbf24",
          "#fcd34d",
          "#d1d5db",
          "#d97706",
          "#9ca3af",
        ],
        borderWidth: 2,
        borderColor: isDark ? "#374151" : "#ffffff",
      },
    ],
  };

  segmentationChart = new Chart(segmentationCtx, {
    type: "doughnut",
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "60%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: isDark ? "#1f2937" : "#ffffff",
          titleColor: isDark ? "#f9fafb" : "#111827",
          bodyColor: isDark ? "#f9fafb" : "#111827",
          borderColor: isDark ? "#374151" : "#e5e7eb",
          borderWidth: 1,
          callbacks: {
            label: (context) => `${context.label}: ${context.parsed}%`,
          },
        },
      },
    },
  });
}

// for promotion pages
let performanceChart; // store chart instance globally

function initPerformanceChart() {
  const performanceCtx = document.getElementById("performance-chart");
  if (!performanceCtx) return;

  const isDark = document.documentElement.classList.contains("dark");

  // Destroy existing chart if it exists
  if (performanceChart) {
    performanceChart.destroy();
  }

  const dates = [];
  const usageData = [];
  const savingsData = [];

  for (let i = 29; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(
      date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    );

    const baseUsage = 15 + Math.sin(i * 0.1) * 8;
    usageData.push(Math.max(0, baseUsage + Math.random() * 10));

    const baseSavings = 800 + Math.sin(i * 0.1) * 200;
    savingsData.push(Math.max(0, baseSavings + Math.random() * 400));
  }

  performanceChart = new Chart(performanceCtx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Promotions Used",
          data: usageData,
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          fill: true,
          tension: 0.4,
          yAxisID: "y",
        },
        {
          label: "Total Savings ($)",
          data: savingsData,
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.1)",
          fill: true,
          tension: 0.4,
          yAxisID: "y1",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: { color: isDark ? "#f9fafb" : "#111827" },
        },
        tooltip: {
          backgroundColor: isDark ? "#1f2937" : "#ffffff",
          titleColor: isDark ? "#f9fafb" : "#111827",
          bodyColor: isDark ? "#f9fafb" : "#111827",
          borderColor: isDark ? "#374151" : "#e5e7eb",
          borderWidth: 1,
        },
      },
      scales: {
        x: {
          grid: { color: isDark ? "#374151" : "#f3f4f6" },
          ticks: { color: isDark ? "#9ca3af" : "#6b7280" },
        },
        y: {
          type: "linear",
          display: true,
          position: "left",
          grid: { color: isDark ? "#374151" : "#f3f4f6" },
          ticks: { color: isDark ? "#9ca3af" : "#6b7280" },
          title: {
            display: true,
            text: "Usage Count",
            color: isDark ? "#9ca3af" : "#6b7280",
          },
        },
        y1: {
          type: "linear",
          display: true,
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: {
            color: isDark ? "#9ca3af" : "#6b7280",
            callback: (value) => "$" + value.toLocaleString(),
          },
          title: {
            display: true,
            text: "Savings ($)",
            color: isDark ? "#9ca3af" : "#6b7280",
          },
        },
      },
      interaction: { intersect: false, mode: "index" },
    },
  });
}

// for analytices pages  // Initialize sales performance chart
function initSalesChart() {
  const salesPerformanceCtx = document.getElementById("sales-performance");
  const isDark = document.documentElement.classList.contains("dark");

  if (!salesPerformanceCtx) return;

  if (salesChart) {
    salesChart.destroy();
  }

  // Generate sample data for the last 30 days
  const dates = [];
  const revenueData = [];
  const ticketsData = [];
  const eventsData = [];

  for (let i = 29; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(
      date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    );

    // Generate realistic data with trends
    const baseRevenue = 5000 + Math.sin(i * 0.1) * 1000;
    revenueData.push(Math.max(0, baseRevenue + (Math.random() - 0.5) * 2000));

    const baseTickets = 100 + Math.sin(i * 0.1) * 30;
    ticketsData.push(Math.max(0, baseTickets + (Math.random() - 0.5) * 40));

    eventsData.push(Math.floor(Math.random() * 5) + 1);
  }

  salesChart = new Chart(salesPerformanceCtx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Revenue ($)",
          data: revenueData,
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          fill: true,
          tension: 0.4,
          yAxisID: "y",
        },
        {
          label: "Tickets Sold",
          data: ticketsData,
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.1)",
          fill: true,
          tension: 0.4,
          yAxisID: "y1",
        },
        {
          label: "Events",
          data: eventsData,
          borderColor: "#8b5cf6",
          backgroundColor: "rgba(139, 92, 246, 0.1)",
          fill: true,
          tension: 0.4,
          yAxisID: "y2",
          hidden: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: isDark ? "#1f2937" : "#ffffff",
          titleColor: isDark ? "#f9fafb" : "#111827",
          bodyColor: isDark ? "#f9fafb" : "#111827",
          borderColor: isDark ? "#374151" : "#e5e7eb",
          borderWidth: 1,
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || "";
              if (label) {
                label += ": ";
              }
              if (context.dataset.label === "Revenue ($)") {
                label += "$" + context.parsed.y.toLocaleString();
              } else {
                label += context.parsed.y.toLocaleString();
              }
              return label;
            },
          },
        },
      },
      scales: {
        x: {
          grid: {
            color: isDark ? "#374151" : "#f3f4f6",
          },
          ticks: {
            color: isDark ? "#9ca3af" : "#6b7280",
          },
        },
        y: {
          type: "linear",
          display: true,
          position: "left",
          grid: {
            color: isDark ? "#374151" : "#f3f4f6",
          },
          ticks: {
            color: isDark ? "#9ca3af" : "#6b7280",
            callback: function (value) {
              return "$" + value.toLocaleString();
            },
          },
        },
        y1: {
          type: "linear",
          display: false,
          position: "right",
          grid: {
            drawOnChartArea: false,
          },
        },
        y2: {
          type: "linear",
          display: false,
          position: "right",
          grid: {
            drawOnChartArea: false,
          },
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
    },
  });
}

function initSalesChart2() {
  const salesChart2Ctx = document.getElementById("sales-chart-2");
  const isDark = document.documentElement.classList.contains("dark");

  if (!salesChart2Ctx) return;

  if (salesChart) salesChart.destroy();

  // 🔒 Static labels (last 7 days example)
  const dates = [
    "Dec 18",
    "Dec 19",
    "Dec 20",
    "Dec 21",
    "Dec 22",
    "Dec 23",
    "Dec 24",
  ];

  // 🔒 Static revenue data
  const revenueData = [
    2200,
    2600,
    2400,
    3000,
    2800,
    3200,
    3500,
  ];

  // 🔒 Static tickets data
  const ticketsData = [
    35,
    42,
    38,
    50,
    46,
    55,
    60,
  ];

  salesChart = new Chart(salesChart2Ctx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Revenue ($)",
          data: revenueData,
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          fill: true,
          tension: 0.4,
          pointBackgroundColor: "#3b82f6",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: "Tickets Sold",
          data: ticketsData,
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.1)",
          fill: true,
          tension: 0.4,
          yAxisID: "y1",
          pointBackgroundColor: "#10b981",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: isDark ? "#1f2937" : "#ffffff",
          titleColor: isDark ? "#f9fafb" : "#111827",
          bodyColor: isDark ? "#f9fafb" : "#111827",
          borderColor: isDark ? "#374151" : "#e5e7eb",
          borderWidth: 1,
          cornerRadius: 8,
        },
      },
      scales: {
        x: {
          ticks: { color: isDark ? "#9ca3af" : "#6b7280" },
          grid: { color: isDark ? "#374151" : "#f3f4f6" },
        },
        y: {
          ticks: {
            color: isDark ? "#9ca3af" : "#6b7280",
            callback: (v) => "$" + v / 1000 + "K",
          },
        },
        y1: {
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: { color: isDark ? "#9ca3af" : "#6b7280" },
        },
      },
    },
  });
}


// Initialize traffic sources chart
let trafficChartInstance;
function initTrafficChart() {
  const trafficChartCtx = document.getElementById("traffic-chart");
  const isDark = document.documentElement.classList.contains("dark");
  if (!trafficChartCtx) return;

  if (trafficChartInstance) {
    trafficChartInstance.destroy();
  }

  trafficChartInstance = new Chart(trafficChartCtx, {
    type: "doughnut",
    data: {
      labels: ["Direct", "Social Media", "Search Engines", "Referrals"],
      datasets: [
        {
          data: [42.3, 28.7, 18.9, 10.1],
          backgroundColor: ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: isDark ? "#1f2937" : "#ffffff",
          titleColor: isDark ? "#f9fafb" : "#111827",
          bodyColor: isDark ? "#f9fafb" : "#111827",
          borderColor: isDark ? "#374151" : "#e5e7eb",
          borderWidth: 1,
          callbacks: {
            label: function (context) {
              return context.label + ": " + context.parsed + "%";
            },
          },
        },
      },
      cutout: "60%",
    },
  });
}
// Initialize marketing performance chart
let marketingChart;
function initMarketingChart() {
  const marketingPerformanceChartCtx = document.getElementById(
    "marketing-performance-chart",
  );
  if (!marketingPerformanceChartCtx) return;
  if(marketingChart){
    marketingChart.destroy();
  }

  const isDark = document.documentElement.classList.contains("dark");

  // Generate sample data for the last 30 days
  const dates = [];
  const emailData = [];
  const affiliateData = [];
  const cartRecoveryData = [];

  for (let i = 29; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(
      date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    );

    emailData.push(800 + Math.sin(i * 0.1) * 200 + Math.random() * 400);
    affiliateData.push(600 + Math.cos(i * 0.1) * 150 + Math.random() * 300);
    cartRecoveryData.push(400 + Math.sin(i * 0.15) * 100 + Math.random() * 200);
  }

  marketingChart = new Chart(marketingPerformanceChartCtx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Email Campaigns",
          data: emailData,
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          fill: true,
          tension: 0.4,
        },
        {
          label: "Affiliate Revenue",
          data: affiliateData,
          borderColor: "#8b5cf6",
          backgroundColor: "rgba(139, 92, 246, 0.1)",
          fill: true,
          tension: 0.4,
        },
        {
          label: "Cart Recovery",
          data: cartRecoveryData,
          borderColor: "#f59e0b",
          backgroundColor: "rgba(245, 158, 11, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: {
            color: isDark ? "#f9fafb" : "#111827",
            usePointStyle: true,
            padding: 20,
          },
        },
        tooltip: {
          backgroundColor: isDark ? "#1f2937" : "#ffffff",
          titleColor: isDark ? "#f9fafb" : "#111827",
          bodyColor: isDark ? "#f9fafb" : "#111827",
          borderColor: isDark ? "#374151" : "#e5e7eb",
          borderWidth: 1,
        },
      },
      scales: {
        x: {
          grid: {
            color: isDark ? "#374151" : "#f3f4f6",
          },
          ticks: {
            color: isDark ? "#9ca3af" : "#6b7280",
          },
        },
        y: {
          grid: {
            color: isDark ? "#374151" : "#f3f4f6",
          },
          ticks: {
            color: isDark ? "#9ca3af" : "#6b7280",
            callback: function (value) {
              return "$" + value.toLocaleString();
            },
          },
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
    },
  });
}

let conversionPieChart;
function initConversionPieChart() {
const conversionPieCtx = document.getElementById("conversionPie");

if (!conversionPieCtx) return;

if(conversionPieChart) conversionPieChart.destroy();

  
  conversionPieChart=new Chart(conversionPieCtx, {
    type: "pie",
    data: {
      labels: ["Converted", "Remaining"],
      datasets: [
        {
          data: [73.5, 26.5],
          backgroundColor: ["#4992eb", "#e5e7eb"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: true,
        },
      },
    },
  });
}

let activityChart;
function initActivityChart(){
 const ctx = document.getElementById('activityChart');

   const getCSSVar = (varName) =>
    getComputedStyle(document.documentElement).getPropertyValue(varName).trim();

  const colors = {
    bar: getCSSVar("--blue-deep"),
    text: getCSSVar("--text"),
    muted: getCSSVar("--muted"),
    grid: getCSSVar("--border"),
    card: getCSSVar("--card"),
  };
  
 if(!ctx) return;

 if(activityChart) activityChart.destroy();

activityChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{
      label: 'User Activity',
      data: [12, 19, 8, 15, 22, 18, 25],
      fill: true,
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: colors.bar,
      tension: 0.3,
      pointBackgroundColor: colors.bar,
      pointRadius: 5,
      pointHoverRadius: 7
    }]
  },
  options: {
    responsive: true,
     maintainAspectRatio: false, 
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: colors.grid,
        titleColor: colors.text,
        bodyColor: colors.text
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 5, color: colors.text },
        grid: { color: colors.grid }
      },
      x: {
        grid: { display: false },
        ticks: { color: colors.text }
      }
    }
  }
});
}
export default function initializeAllCharts() {
  salesAnalyticsChart?.();
  initCharts?.();
  initSegmentationChart?.();
  initPerformanceChart?.();
  initSalesChart?.();
  initSalesChart2?.();
  initTrafficChart?.();
  initMarketingChart?.();
  initConversionPieChart?.();
  initMonthlyBarChart?.();
  initDonutChart?.();
  initPayoutTrendChart?.();
  initActivityChart?.();
}
