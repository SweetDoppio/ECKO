document.addEventListener("DOMContentLoaded", function () {
  // PDF Export
  const pdfButton = document.getElementById("pdfExportButton");
  if (pdfButton) {
    pdfButton.addEventListener("click", () => {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const content = document.getElementById("report-content")?.innerText || "";
      doc.text(content, 10, 10);
      doc.save("report.pdf");
    });
  }

  // CSV Export
  const csvButton = document.getElementById("csvExportButton");
  if (csvButton) {
    csvButton.addEventListener("click", () => {
      const findings = document.querySelectorAll("#report-content .finding");
      let csv = "Title,Risk,Status\n";

      findings.forEach(f => {
        const title = f.querySelector("strong")?.innerText || "";
        const risk = f.querySelector("span")?.innerText || "";
        const statusText = Array.from(f.querySelectorAll("p"))
          .find(p => p.innerText.startsWith("Status:"))?.innerText || "";
        const status = statusText.split(":")[1]?.trim() || "";
        csv += `"${title}","${risk}","${status}"\n`;
      });

      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "report.csv";
      a.click();
      URL.revokeObjectURL(url);
    });
  }
});
