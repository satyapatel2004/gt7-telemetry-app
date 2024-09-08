import { Box, Typography } from '@mui/material';

function LapTimes({ lapData }) {
  return (
    <Box sx={{ backgroundColor: '#333', padding: '10px', borderRadius: '10px', height: '100%' }}>
      <Typography variant="h6" sx={{ textAlign: 'center' }}>Lap Times</Typography>
      <Box sx={{ maxHeight: '200px', overflowY: 'auto' }}>
        {lapData.map((lap, index) => (
          <Box key={index} sx={{ marginBottom: '10px', padding: '5px', backgroundColor: '#222', borderRadius: '5px' }}>
            <Typography variant="body1" sx={{ color: 'cyan' }}>Lap {lap.lapno}</Typography>
            <Typography variant="body2" sx={{ color: 'white' }}>Lap Time: {lap.laptime}</Typography>
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default LapTimes;
