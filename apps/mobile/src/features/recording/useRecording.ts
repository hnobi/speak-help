import { useCallback, useState } from 'react';

export function useRecording() {
  const [isRecording, setIsRecording] = useState(false);
  const [durationSeconds, setDurationSeconds] = useState(0);

  const start = useCallback(() => {
    setIsRecording(true);
    setDurationSeconds(0);
  }, []);

  const stop = useCallback(() => {
    setIsRecording(false);
  }, []);

  const tick = useCallback(() => {
    setDurationSeconds((current) => current + 1);
  }, []);

  return {
    isRecording,
    durationSeconds,
    start,
    stop,
    tick,
  };
}
