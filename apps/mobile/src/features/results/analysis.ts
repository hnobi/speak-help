export type AnalysisStatus = 'uploaded' | 'processing' | 'done' | 'failed';

export interface AnalysisSummary {
  recordingId: string;
  transcript: string;
  overallScore: number;
  status: AnalysisStatus;
}

export function buildAnalysisSummary(recordingId: string, transcript: string): AnalysisSummary {
  return {
    recordingId,
    transcript,
    overallScore: 88,
    status: 'done',
  };
}
