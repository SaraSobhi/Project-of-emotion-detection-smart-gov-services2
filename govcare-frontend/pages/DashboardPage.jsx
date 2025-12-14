import { Grid, Box, Typography } from "@mui/material";
import StatCard from "../components/StatCard";
import ComplaintsTable from "../components/ComplaintsTable"; 

const Dashboard = () => {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #1e1b4b, #020617)",
        px: 10, 
        py: 10, 
      }}
    >
      <Typography
        variant="h4"
        sx={{ color: "white", mb: 4 }}
      >
        Dashboard Overview
      </Typography>

      {/* ====== STAT CARDS - تم التعديل هنا لـ md={3} (ربع عرض الشاشة) ====== */}
      <Grid container spacing={20} sx={{ width: "100%" }}> {/* عدت الـ spacing إلى 3 */}
        <Grid item xs={12} sm={6} md={20}> {/* التعديل: 3 من 12 */}
          <StatCard title="إجمالي الشكاوى" value={120} />
        </Grid>
        <Grid item xs={12} sm={6} md={20}> {/* التعديل: 3 من 12 */}
          <StatCard title="الشكاوى المحلولة" value={45} />
        </Grid>
        <Grid item xs={12} sm={6} md={20}> {/* التعديل: 3 من 12 */}
          <StatCard title="قيد المعالجة" value={300} />
        </Grid>
        <Grid item xs={12} sm={6} md={20}> {/* التعديل: 3 من 12 */}
          <StatCard title="شكاوى جديدة" value={45} />
        </Grid>
      </Grid>

      <Box sx={{ mt: 5 }}>
        <ComplaintsTable />
      </Box>
    </Box>
  );
};

export default Dashboard;