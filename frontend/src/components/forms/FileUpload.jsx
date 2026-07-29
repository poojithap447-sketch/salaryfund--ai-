import { useCallback, useState } from 'react'
import { FileText, UploadCloud, X } from 'lucide-react'
import { cn } from '@/utils/cn'

export default function FileUpload({ label, accept = '.pdf,.jpg,.jpeg,.png', multiple = false, onFilesChange }) {
  const [files, setFiles] = useState([])
  const [isDragging, setIsDragging] = useState(false)

  const handleFiles = useCallback(
    (fileList) => {
      const next = multiple ? [...files, ...Array.from(fileList)] : Array.from(fileList).slice(0, 1)
      setFiles(next)
      onFilesChange?.(next)
    },
    [files, multiple, onFilesChange]
  )

  function removeFile(idx) {
    const next = files.filter((_, i) => i !== idx)
    setFiles(next)
    onFilesChange?.(next)
  }

  return (
    <div>
      {label && <p className="mb-2 text-sm font-medium">{label}</p>}
      <label
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setIsDragging(false)
          handleFiles(e.dataTransfer.files)
        }}
        className={cn(
          'flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed px-6 py-8 text-center transition-colors',
          isDragging ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
        )}
      >
        <input
          type="file"
          accept={accept}
          multiple={multiple}
          className="hidden"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />
        <UploadCloud className="h-6 w-6 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          <span className="font-medium text-primary">Click to upload</span> or drag and drop
        </p>
        <p className="text-xs text-muted-foreground/70">PDF, JPG or PNG, up to 10MB</p>
      </label>

      {files.length > 0 && (
        <ul className="mt-3 space-y-2">
          {files.map((file, idx) => (
            <li key={idx} className="flex items-center justify-between rounded-lg bg-secondary/50 px-3 py-2 text-sm">
              <span className="flex items-center gap-2 truncate">
                <FileText className="h-4 w-4 shrink-0 text-muted-foreground" />
                <span className="truncate">{file.name}</span>
              </span>
              <button type="button" onClick={() => removeFile(idx)} className="text-muted-foreground hover:text-danger">
                <X className="h-4 w-4" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
