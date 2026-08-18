 import 'warrant.dart';

class Choice {
  final Warrant w;
  final double score;

  Choice(this.w, this.score);
}

class WarrantSelector {
  List<Choice> select(
    List<Warrant> warrants,
    String underlying,
    String direction,
  ) {
    final choices = warrants
        .where(
          (w) =>
              w.underlying == underlying &&
              w.direction == direction &&
              (w.daysToExpiry ?? 0) > 3,
        )
        .map((w) {
          final delta = (w.delta ?? 0).abs().clamp(0.0, 1.0).toDouble();

          final leverage =
              (w.leverage ?? 0).clamp(0.0, 15.0).toDouble();

          final volume = (w.volume ?? 0).toDouble();

          final spread =
              (w.spreadPct ?? 0).clamp(0.0, 10.0).toDouble();

          final score =
              delta * 35 +
              (leverage / 15) * 30 +
              (volume > 0 ? 20 : 0) +
              10 -
              (spread / 10) * 20;

          return Choice(w, score);
        })
        .toList();

    choices.sort((a, b) => b.score.compareTo(a.score));

    return choices.take(5).toList();
  }
}
