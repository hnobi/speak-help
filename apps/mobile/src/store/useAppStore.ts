import { create } from 'zustand';

interface AppState {
  isRecording: boolean;
  recordingDuration: number;
  setIsRecording: (value: boolean) => void;
  setRecordingDuration: (value: number) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isRecording: false,
  recordingDuration: 0,
  setIsRecording: (value) => set({ isRecording: value }),
  setRecordingDuration: (value) => set({ recordingDuration: value }),
}));
