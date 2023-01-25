Mix.install([
  {:jason, "~> 1.2"}
])

file = "version.json"

cv = File.read!(file) |> Jason.decode!()

nv = Version.parse!(cv["version"])
IO.puts("Current version: #{Version.to_string(nv)}")

nv = %{nv | minor: nv.minor + 1}
sv = Version.to_string(nv)

IO.puts("   Next version: #{sv}")

ver = Map.put(cv, "version", sv) |> Jason.encode!(pretty: true)
File.write(file, ver)