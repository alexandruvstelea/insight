import HeaderSection from "../HeaderSection";

export default function ReportForm() {
  return (
    <>
      <div className="w-full mt-20 p-4 flex justify-center items-center flex-col ">
        <div className="max-w-2xl w-full bg-slate-700 p-4 rounded ">
          <HeaderSection count={false} title="Raportează bug" />
          <form>
            <div className="mb-5">
              <label htmlFor="name" className="label">
                Nume
              </label>
              <input
                type="text"
                id="name"
                name="name"
                placeholder="Nume"
                className="input"
              />
            </div>
            <div className="mb-5">
              <label htmlFor="bugDescription" className="label">
                Descrierea bug-ului *
              </label>
              <textarea
                id="bugDescription"
                name="bugDescription"
                rows={6}
                placeholder="Descrie bug-ul in detaliu"
                className="input"
              />
            </div>
            <button type="submit" className="button w-full">
              Trimite raportul
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
