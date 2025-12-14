import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from "@mui/material";

const complaints = [
  {
    text: "الخدمة سيئة جداً",
    sentiment: "Negative",
    confidence: 92,
    status: "New",
  },
  {
    text: "الخدمة ممتازة",
    sentiment: "Positive",
    confidence: 88,
    status: "Resolved",
  },
];

const ComplaintsTable = () => {
  return (
    <TableContainer
      component={Paper}
      sx={{
        background: "rgba(255,255,255,0.06)",
        backdropFilter: "blur(10px)",
        borderRadius: 4,
        boxShadow: "0 8px 24px rgba(0,0,0,0.3)",
        mt: 4,
      }}
    >
      <Table>
        {/* ===== TABLE HEADER ===== */}
        <TableHead>
          <TableRow>
            <TableCell sx={{ color: "#e5e7eb", fontWeight: "bold" }}>
              الشكوى
            </TableCell>
            <TableCell sx={{ color: "#e5e7eb", fontWeight: "bold" }}>
              Sentiment
            </TableCell>
            <TableCell sx={{ color: "#e5e7eb", fontWeight: "bold" }}>
              Confidence
            </TableCell>
            <TableCell sx={{ color: "#e5e7eb", fontWeight: "bold" }}>
              Status
            </TableCell>
          </TableRow>
        </TableHead>

        {/* ===== TABLE BODY ===== */}
        <TableBody>
          {complaints.map((row, index) => (
            <TableRow
              key={index}
              sx={{
                "&:hover": {
                  backgroundColor: "rgba(255,255,255,0.08)",
                },
              }}
            >
              <TableCell sx={{ color: "#f9fafb" }}>
                {row.text}
              </TableCell>

              <TableCell>
                <Chip
                  label={row.sentiment}
                  color={row.sentiment === "Positive" ? "success" : "error"}
                  size="small"
                />
              </TableCell>

              <TableCell sx={{ color: "#f9fafb" }}>
                {row.confidence}%
              </TableCell>

              <TableCell>
                <Chip
                  label={row.status}
                  variant="outlined"
                  size="small"
                  color={
                    row.status === "Resolved"
                      ? "success"
                      : row.status === "In Progress"
                      ? "warning"
                      : "info"
                  }
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ComplaintsTable;
