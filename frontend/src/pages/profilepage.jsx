export default function ProfilePage() {
  return (
    <div className="max-w-md mx-auto py-12 px-6">
      <h2 className="text-xl font-semibold mb-6 text-center">Profile</h2>

      <div className="mb-6">
        <p className="mb-2 font-medium">Age</p>
        <div className="space-y-2">
          <label className="flex items-center gap-2">
            <input type="radio" name="age" /> Under 18
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" name="age" /> 18–64 (Adults)
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" name="age" /> 64+ (Older Adults)
          </label>
        </div>
      </div>

      <div className="mb-6">
        <p className="mb-2 font-medium">Gender</p>
        <div className="space-y-2">
          <label className="flex items-center gap-2">
            <input type="radio" name="gender" /> Male
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" name="gender" /> Female
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" name="gender" /> Other
          </label>
        </div>
      </div>
      <div>
        <label className="block mb-2 font-medium">Symptoms:</label>
        <textarea
          rows="3"
          placeholder="e.g. chest pain, headache..."
          className="w-full p-3 border border-gray-300 rounded-md"
        ></textarea>
      </div>
    </div>
  );
}
