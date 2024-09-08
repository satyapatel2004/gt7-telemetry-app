import { Box, Typography } from '@mui/material';

function ThrottleDisplay({ throttle }) {
  return (
    <Box sx={{ backgroundColor: '#333', padding: '10px', borderRadius: '10px', textAlign: 'center' }}>
      <Typography variant="h6">Throttle</Typography>
      <Typography 
        variant="h4" 
        sx={{ 
          color: 'limegreen', 
          transition: 'all 0.5s ease-out', // Smooth transition
        }}
      >
      </Typography>
    </Box>
  );
}

export default ThrottleDisplay;
