import { Box } from '@mui/material';

function LEDBar({ throttle }) {
  return (
    <Box sx={{ 
        width: '100%', 
        maxWidth: '500px', 
        height: '30px', 
        backgroundColor: '#111',  // Dark background for contrast
        borderRadius: '4px',  // Less rounded for a boxy look
        overflow: 'hidden', 
        boxShadow: '0px 0px 10px 3px rgba(0, 0, 0, 0.6)',
        border: '2px solid #222',  // Slight border for structure
        position: 'relative',
        }}>
      
      {/* Filled part of the bar */}
      <Box sx={{ 
          width: `${throttle}%`,  // Proportional to the throttle value
          height: '100%', 
          background: 'linear-gradient(90deg, rgba(0,0,139,1) 0%, rgba(0,191,255,1) 100%)', // Dark blue to neon blue
          transition: 'width 0.3s ease',  // Smooth movement
          boxShadow: '0px 0px 10px 2px rgba(0, 191, 255, 0.8)',  // Neon blue glow effect
        }}
      />

      {/* Marker for maximum throttle */}
      <Box sx={{
          position: 'absolute',
          top: '0',
          right: '0',
          width: '4px',
          height: '100%',
          backgroundColor: 'rgba(0, 191, 255, 0.8)',
        }}
      />
    </Box>
  );
}

export default LEDBar;