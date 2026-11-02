# CLAUDE.md — robotika-tanpa-lab (PUBLIC)

Free, public part of "Lab Robotika Tanpa Lab": an Indonesian-language, simulation-first
robotics & AI course (ROS 2 Jazzy + Gazebo Harmonic on ordinary laptops, no Isaac Sim).
This repo holds the README, syllabus, Modul 0–2 with exercises and solutions,
`course/kode/cek_lab.sh`, the `rtl_dasar` ROS 2 package, the LaTeX template and build script.

## Rules
- Course material is written in **Bahasa Indonesia**; discussion in English.
- Schedules in course material are in **WIB**.
- This repo is public: keep it to free course material only. **No prices, no business,
  sales or planning documents.** Use `\tbd{harga}` in LaTeX and "TBD" in Markdown where a
  price would appear.
- Before every push: `git grep -nE 'Rp|[0-9]{1,3}(\.[0-9]{3}){2,}'` must return nothing
  relevant — stop and ask if it does.
- `latex/rtl.cls` and `scripts/build-pdf.sh` here are the **source of truth** for the
  template; other repos copy them (no submodules).
- All documents use `latex/rtl.cls`; build with `./scripts/build-pdf.sh` (outputs to `pdf/`).
  The GitHub Action is manual-only; commit built PDFs.
- Code: ROS 2 Jazzy, Python `rclpy`, ament_python. Test on real ROS 2 before committing;
  `colcon test` / flake8 must pass.
- Ask before big decisions (naming, tools, licenses) and before anything destructive
  (force-push, deleting files).
- After each deliverable: commit, push, and summarise the change in 1–2 lines.
