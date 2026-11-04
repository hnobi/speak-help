import { StyleSheet, Text, View, Pressable } from 'react-native';
import { useAppStore } from '@/store/useAppStore';
import { useRecording } from '@/features/recording/useRecording';

export default function HomeScreen() {
  const { isRecording, recordingDuration, setIsRecording, setRecordingDuration } = useAppStore();
  const { start, stop, tick, durationSeconds } = useRecording();

  const handlePress = () => {
    const next = !isRecording;
    setIsRecording(next);
    setRecordingDuration(durationSeconds);
    if (next) {
      start();
      const interval = setInterval(() => {
        tick();
        setRecordingDuration(durationSeconds + 1);
      }, 1000);
      setTimeout(() => clearInterval(interval), 60000);
    } else {
      stop();
      setRecordingDuration(durationSeconds);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Speaking Coach</Text>
      <Text style={styles.subtitle}>Record a 60–120 second practice prompt.</Text>
      <Text style={styles.stats}>Status: {isRecording ? 'Recording' : 'Ready'}</Text>
      <Text style={styles.stats}>Duration: {durationSeconds}s</Text>
      <Pressable style={styles.button} onPress={handlePress}>
        <Text style={styles.buttonText}>{isRecording ? 'Stop recording' : 'Start recording'}</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#121826',
    padding: 24,
  },
  title: {
    color: '#f8fafc',
    fontSize: 32,
    fontWeight: '700',
    marginBottom: 12,
  },
  subtitle: {
    color: '#cbd5e1',
    fontSize: 16,
    marginBottom: 16,
  },
  stats: {
    color: '#e2e8f0',
    fontSize: 18,
    marginBottom: 8,
  },
  button: {
    marginTop: 24,
    backgroundColor: '#38bdf8',
    borderRadius: 999,
    paddingHorizontal: 24,
    paddingVertical: 14,
  },
  buttonText: {
    color: '#04111d',
    fontSize: 18,
    fontWeight: '700',
  },
});
