// Extract still frames from a build video with AVFoundation (no ffmpeg needed), for studying how a kit is built.
//   swiftc -O tools/video/frames.swift -o <somewhere>/frames        (compile once; running it with "swift" is slow)
//   frames <video> <out dir> <whole seconds between frames> [max dimension px] [start s] [end s]
// Files are named tMMmSSs.jpg by video time. Prints the video's duration. tools/video/sheets.py makes contact sheets.
// Each frame is decoded inside an autoreleasepool: without it the process grows by gigabytes on a long video.
import AVFoundation
import AppKit
let a = CommandLine.arguments
let url = URL(fileURLWithPath: a[1]), out = URL(fileURLWithPath: a[2])
let every = max(1.0, Double(a[3]) ?? 5), maxW = a.count > 4 ? (Double(a[4]) ?? 960) : 960
let asset = AVURLAsset(url: url)
let dur = CMTimeGetSeconds(asset.duration)
let start = a.count > 5 ? (Double(a[5]) ?? 0) : 0, end = a.count > 6 ? min(Double(a[6]) ?? dur, dur) : dur
try? FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.maximumSize = CGSize(width: maxW, height: maxW)
let tol = CMTime(seconds: min(0.5, every / 4), preferredTimescale: 600)
gen.requestedTimeToleranceBefore = tol
gen.requestedTimeToleranceAfter = tol
var t = start, n = 0
print(String(format: "duration %.1f s", dur))
while t <= end {
  autoreleasepool {                       // without this every decoded frame stays in memory until the end
    if let cg = try? gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil) {
      let rep = NSBitmapImageRep(cgImage: cg)
      if let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.72]) {
        let m = Int(t) / 60, s = Int(t) % 60
        try? data.write(to: out.appendingPathComponent(String(format: "t%02dm%02ds.jpg", m, s)))
        n += 1
      }
    }
  }
  t += every
}
print("wrote \(n) frames")
