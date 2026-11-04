import { buildAnalysisSummary } from './analysis';

describe('buildAnalysisSummary', () => {
  it('returns a completed summary with the transcript', () => {
    const summary = buildAnalysisSummary('rec_123', 'I learn English every day.');
    expect(summary.recordingId).toBe('rec_123');
    expect(summary.transcript).toBe('I learn English every day.');
    expect(summary.overallScore).toBe(88);
    expect(summary.status).toBe('done');
  });
});
