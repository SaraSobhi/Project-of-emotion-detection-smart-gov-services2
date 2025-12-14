import { Card, CardContent, Typography } from "@mui/material";

const StatCard = ({ title, value }) => {
  return (
    <Card
      sx={{
        width: "100%", 
        height: "100%", 
        background: "rgba(255,255,255,0.08)",
        backdropFilter: "blur(10px)",
        borderRadius: 4,
        color: "white",
        // زيادة الـ box shadow لتأثير أكثر بروزًا
        boxShadow: "0 8px 32px 0 rgba(31, 38, 135, 0.37)", 
      }}
    >
      {/* زيادة الـ padding لـ CardContent لجعل الكارد يبدو أكبر */}
      <CardContent sx={{ p: 3 }}> 
        
        {/* عنوان الكارد - زيادة حجم الخط قليلاً */}
        <Typography 
          variant="h6" // تم تغييرها من body2 إلى h6
          sx={{ opacity: 0.8, mb: 1 }}
        >
          {title}
        </Typography>
        
        {/* القيمة الرئيسية - زيادة كبيرة في حجم الخط */}
        <Typography 
          variant="h2" // تم تغييرها من h3 إلى h2 (لجعل الرقم كبيراً)
          fontWeight="bold"
        >
          {value}
        </Typography>
        
      </CardContent>
    </Card>
  );
};

export default StatCard;