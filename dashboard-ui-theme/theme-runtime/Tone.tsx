import type { Tone } from "../lib/format";

const TONE_CLASSES: Record<Tone, string> = {
  good: "text-[var(--color-good)] bg-[var(--color-good-soft)]",
  warn: "text-[var(--color-warn)] bg-[var(--color-warn-soft)]",
  bad: "text-[var(--color-bad)] bg-[var(--color-bad-soft)]",
  neutral: "text-(--color-ink-muted) bg-(--color-line)/40",
};

export function ToneBadge({ tone, children }: { tone: Tone; children: React.ReactNode }) {
  return (
    <span
      className={`inline-flex items-center rounded-sm px-1.5 py-0.5 text-xs font-semibold tabular-nums ${TONE_CLASSES[tone]}`}
    >
      {children}
    </span>
  );
}

export function toneDot(tone: Tone): string {
  return (
    {
      good: "bg-[var(--color-good)]",
      warn: "bg-[var(--color-warn)]",
      bad: "bg-[var(--color-bad)]",
      neutral: "bg-(--color-ink-muted)",
    } satisfies Record<Tone, string>
  )[tone];
}
